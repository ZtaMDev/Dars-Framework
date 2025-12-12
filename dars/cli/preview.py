#!/usr/bin/env python3
"""
Dars Preview - Optimized Preview Server for Dars Applications
Fast, reliable server specifically designed for hot reload development.
"""

import os
import sys
import webbrowser
import http.server
import mimetypes
import socketserver
import threading
import time
from pathlib import Path
from urllib.parse import urlparse
import signal

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


class PreviewServer:
    """Fast preview server optimized for hot reload development"""

    class FastRequestHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.base_directory = kwargs.pop("directory", ".")
            super().__init__(*args, **kwargs)

        def translate_path(self, path):
            # Override to serve from our specific directory
            path = super().translate_path(path)
            relpath = os.path.relpath(path, os.getcwd())
            return os.path.join(self.base_directory, relpath)

        def do_GET(self):
            # Handle query parameters
            path_no_query = self.path.split('?')[0]

            # Hot reload endpoints - serve immediately with no caching
            if path_no_query.endswith("version.txt") or (
                path_no_query.startswith("/version_") and path_no_query.endswith(".txt")
            ):
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
                self.send_header("Pragma", "no-cache")
                self.send_header("Expires", "0")
                self.end_headers()

                version_path = self.translate_path(path_no_query)
                if os.path.exists(version_path):
                    with open(version_path, "r") as f:
                        self.wfile.write(f.read().encode())
                else:
                    self.wfile.write(b"0")
                return

            # For root path, always serve index.html
            if path_no_query == "/" or path_no_query == "":
                self.path = "/index.html"

            # Check if file exists, if not serve index.html for SPA routing
            file_path = self.translate_path(self.path)
            if not os.path.exists(file_path):
                index_path = os.path.join(self.base_directory, "index.html")
                if os.path.exists(index_path):
                    self.path = "/index.html"
                else:
                    self.send_error(404, "File not found")
                    return

            return super().do_GET()

        def end_headers(self):
            # Development headers - no caching
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            super().end_headers()

        def guess_type(self, path):
            # Ensure correct MIME types
            if path.endswith(".mjs") or path.endswith(".js"):
                return "application/javascript"
            if path.endswith(".json"):
                return "application/json"
            if path.endswith(".css"):
                return "text/css"
            if path.endswith(".html"):
                return "text/html"
            return super().guess_type(path)

        def log_message(self, format, *args):
            try:
                # Suppress logs for hot reload requests and normal page loads
                path = getattr(self, "path", "")
                
                # Fallback to requestline if path is empty
                if not path and hasattr(self, 'requestline'):
                    parts = self.requestline.split()
                    if len(parts) > 1:
                        path = parts[1]
                
                # Handle query parameters by splitting at '?'
                clean_path = path.split('?')[0]
                
                if ("version" in clean_path and clean_path.endswith('.txt')) or any(
                    pattern in path
                    for pattern in ["favicon.ico", ".css", ".js", ".png", ".jpg", ".svg"]
                ):
                    return
                
                # Handle different log message formats safely
                if len(args) >= 3:
                    # Normal request: (client_address, method, request_line)
                    console.print(f"[dim]HTTP {args[1]} {args[0]} - {args[2]}[/dim]")
                elif len(args) == 2:
                    # Error message: (code, message)
                    console.print(f"[dim]HTTP Error {args[0]}: {args[1]}[/dim]")
                else:
                    # Unknown format, log what we have
                    console.print(f"[dim]HTTP Log: {args}[/dim]")
            except Exception:
                # Silently ignore any logging errors during shutdown
                pass

    def __init__(self, directory: str, port: int = 8000, host: str = "localhost"):
        self.directory = os.path.abspath(directory)
        self.port = port
        self.host = host
        self.server = None
        self.server_thread = None
        self._is_ready = False
        self._shutdown_event = threading.Event()
        self._server_stopped = False

    def is_ready(self):
        """Check if index.html exists and server is ready"""
        index_path = os.path.join(self.directory, "index.html")
        return os.path.exists(index_path) and self._is_ready

    def wait_until_ready(self, timeout=5.0):
        """Wait for index.html to be available"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            index_path = os.path.join(self.directory, "index.html")
            if os.path.exists(index_path):
                return True
            time.sleep(0.05)
        return False

    def start(self):
        """Starts the preview server - optimized for fast startup"""
        try:
            # Ensure directory exists
            os.makedirs(self.directory, exist_ok=True)

            # Register mimetypes
            mimetypes.add_type("application/javascript", ".js")
            mimetypes.add_type("application/javascript", ".mjs")
            mimetypes.add_type("application/json", ".json")

            # Use ThreadingTCPServer to allow concurrent requests and clean shutdown
            handler = lambda *args, **kwargs: self.FastRequestHandler(
                *args, directory=self.directory, **kwargs
            )

            # Ensure the class allows reuse address before bind
            socketserver.ThreadingTCPServer.allow_reuse_address = True
            self.server = socketserver.ThreadingTCPServer((self.host, self.port), handler)

            # Don't block process exit for active request threads
            self.server.daemon_threads = True

            # Start server in a background thread using serve_forever with a short poll interval
            self.server_thread = threading.Thread(target=self._serve_forever)
            self.server_thread.daemon = True  # Changed to True for faster shutdown
            self.server_thread.start()

            # mark ready quickly
            time.sleep(0.05)
            self._is_ready = True

            console.print(f"[green]OK Preview server started on http://{self.host}:{self.port}[/green]")
            return True

        except Exception as e:
            console.print(f"[red]Failed to start preview server: {e}[/red]")
            return False

    def _serve_forever(self):
        """Serve forever with proper shutdown handling"""
        try:
            self.server.serve_forever(poll_interval=0.5)
        except Exception:
            # Ignore errors during shutdown
            if not self._shutdown_event.is_set():
                pass

    def stop(self, timeout: float = 2.0):
        """Stops the preview server quickly and reliably"""
        if self._server_stopped:
            return
            
        self._shutdown_event.set()
        self._is_ready = False
        self._server_stopped = True

        if self.server:
            try:
                # First shutdown the server to stop accepting new connections
                self.server.shutdown()
            except Exception:
                pass

            try:
                # Then close the server socket
                self.server.server_close()
            except Exception:
                pass

            self.server = None

        # Wait for thread to finish with timeout
        if self.server_thread and self.server_thread.is_alive():
            self.server_thread.join(timeout=timeout)

        # If still alive after timeout, it will be killed as daemon thread
        if self.server_thread and self.server_thread.is_alive():
            console.print("[yellow]Server thread stopping...[/yellow]")

    def get_url(self) -> str:
        """Gets the server URL"""
        return f"http://{self.host}:{self.port}"


def preview_app(directory: str, auto_open: bool = True, port: int = 8000, host: str = "localhost"):
    """Previews a Dars HTML application with fast hot reload support"""

    # Verify that directory exists
    if not os.path.exists(directory):
        console.print(f"[red]Directory does not exist: {directory}[/red]")
        return False

    # Create and start the server
    server = PreviewServer(directory, port, host=host)

    if not server.start():
        return False

    url = server.get_url()

    # Show information
    panel = Panel(
        Text(
            f"Preview server running successfully\n\n"
            f"URL: {url}\n"
            f"Directory: {directory}\n"
            f"Port: {port}\n\n"
            f"Press Ctrl+C to stop the server",
            style="bold green",
            justify="center",
        ),
        title="Dars Preview",
        border_style="cyan",
    )
    console.print(panel)

    # Open in browser if requested
    if auto_open:
        try:
            webbrowser.open(url)
            console.print(f"[cyan]Opening in browser: {url}[/cyan]")
        except Exception as e:
            console.print(f"[yellow]Could not open browser: {e}[/yellow]")
            console.print(f"[cyan]Open manually: {url}[/cyan]")

    # Improved shutdown handling
    def signal_handler(sig, frame):
        console.print(f"\n[yellow]Stopping preview server...[/yellow]")
        # Stop server immediately
        server.stop()
        console.print(f"[green]OK Preview server stopped successfully[/green]")
        # Exit cleanly
        sys.exit(0)

    try:
        signal.signal(signal.SIGINT, signal_handler)
    except Exception as e:
        console.print(f"[yellow]Warning: Could not set signal handler: {e}[/yellow]")

    try:
        # Keep the main thread alive with polling
        while server._is_ready and not server._shutdown_event.is_set():
            time.sleep(0.1)
    except KeyboardInterrupt:
        signal_handler(None, None)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        server.stop()

    return True


def main():
    """Main entry point for the preview server"""
    import argparse

    parser = argparse.ArgumentParser(description="Dars Preview Server")
    parser.add_argument("directory", help="Directory containing the exported application")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Port to run the server on (default: 8000)")
    parser.add_argument("--host", type=str, default="localhost", help="Host to bind to (default: localhost)")
    parser.add_argument("--no-open", action="store_true", help="Do not open browser automatically")

    args = parser.parse_args()

    success = preview_app(args.directory, auto_open=not args.no_open, port=args.port, host=args.host)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()