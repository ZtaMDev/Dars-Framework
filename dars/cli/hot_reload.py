import os
import time
import threading
import importlib
from pathlib import Path

class FileWatcher:
    """Watches a file for changes and triggers a callback when it changes."""
    def __init__(self, path, on_change, poll_interval=0.5):
        self.path = path
        self.on_change = on_change
        self.poll_interval = poll_interval
        self._last_mtime = None
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._watch, daemon=True)

    def start(self):
        try:
            self._last_mtime = os.path.getmtime(self.path)
        except OSError:
            # File might not exist yet, we'll check in the watch loop
            self._last_mtime = None
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()

    def _watch(self):
        while not self._stop_event.is_set():
            try:
                if os.path.exists(self.path):
                    mtime = os.path.getmtime(self.path)
                    if mtime != self._last_mtime:
                        self._last_mtime = mtime
                        self.on_change()
                else:
                    # File was deleted, reset last_mtime so we detect when it's recreated
                    if self._last_mtime is not None:
                        self._last_mtime = None
            except Exception:
                pass
            time.sleep(self.poll_interval)

class DirectoryWatcher:
    """Watches a directory for file changes and new files."""
    def __init__(self, directory, extensions, on_change, poll_interval=1.0):
        self.directory = directory
        self.extensions = extensions
        self.on_change = on_change
        self.poll_interval = poll_interval
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._watch, daemon=True)
        self._known_files = self._get_current_files()

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()

    def _get_current_files(self):
        """Get current files matching extensions in directory."""
        files = set()
        try:
            for ext in self.extensions:
                for file_path in Path(self.directory).rglob(f"*{ext}"):
                    if self._should_watch_file(file_path):
                        files.add(str(file_path))
        except Exception:
            pass
        return files

    def _should_watch_file(self, file_path):
        """Check if file should be watched based on exclusion rules."""
        skip_dirs = {"__pycache__", ".git", "dars_preview", ".pytest_cache", "venv", "env", "node_modules"}
        file_str = str(file_path)
        return not any(skip_dir in file_str for skip_dir in skip_dirs)

    def _watch(self):
        while not self._stop_event.is_set():
            try:
                current_files = self._get_current_files()
                
                # Check for new files
                new_files = current_files - self._known_files
                if new_files:
                    if len(new_files) == 1:
                        file = next(iter(new_files))
                        self.on_change(f"New file created: {os.path.relpath(file, self.directory)}")
                    else:
                        self.on_change(f"New files detected: {len(new_files)} files")
                    self._known_files = current_files
                
                # Check for deleted files (optional, but good for tracking)
                deleted_files = self._known_files - current_files
                if deleted_files:
                    self._known_files = current_files
                    
            except Exception as e:
                # Log error but continue watching
                pass
                
            time.sleep(self.poll_interval)

class EnhancedFileWatcher:
            """Watches a file for changes and triggers a callback when it changes."""
            def __init__(self, path, on_change, poll_interval=0.5):
                self.path = path
                self.on_change = on_change
                self.poll_interval = poll_interval
                self._last_mtime = None
                self._stop_event = threading.Event()
                self._thread = threading.Thread(target=self._watch, daemon=True)

            def start(self):
                try:
                    self._last_mtime = os.path.getmtime(self.path)
                except OSError:
                    # File might not exist yet, we'll check in the watch loop
                    self._last_mtime = None
                self._thread.start()

            def stop(self):
                self._stop_event.set()
                self._thread.join()

            def _watch(self):
                while not self._stop_event.is_set():
                    try:
                        if os.path.exists(self.path):
                            mtime = os.path.getmtime(self.path)
                            if mtime != self._last_mtime:
                                self._last_mtime = mtime
                                self.on_change()
                        else:
                            # File was deleted, reset last_mtime so we detect when it's recreated
                            if self._last_mtime is not None:
                                self._last_mtime = None
                    except Exception:
                        pass
                    time.sleep(self.poll_interval)