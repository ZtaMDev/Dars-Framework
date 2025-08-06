import os
import time
import threading
import importlib

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
        self._last_mtime = os.path.getmtime(self.path)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()

    def _watch(self):
        while not self._stop_event.is_set():
            try:
                mtime = os.path.getmtime(self.path)
                if mtime != self._last_mtime:
                    self._last_mtime = mtime
                    self.on_change()
            except Exception:
                pass
            time.sleep(self.poll_interval)
