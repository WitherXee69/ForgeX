"""UI/backend boundary.

Replace the demo methods here with calls into ForgeX's real backend. Keep network
work off the GUI thread (QThreadPool/QRunnable or a worker QObject) and emit
signals back to the UI. The widgets intentionally know nothing about requests,
GitHub headers, recipe parsing, or installation internals.
"""
from __future__ import annotations

from PySide6.QtCore import QObject, Signal, QTimer

from core.engine import Engine


class ForgeXController(QObject):
    search_finished = Signal(list)
    repository_loaded = Signal(dict)
    install_progress = Signal(int, str)
    install_finished = Signal(bool, str)
    status_changed = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, parent=None, engine=None, context=None):
        super().__init__(parent)

        self.engine = engine
        self.context = context

        self.authenticated = False
        self.username = ""
        self._demo_install_timer = None

    def login(self, username: str, token: str) -> None:
        """Store GitHub credentials for subsequent API requests."""
        self.authenticated = bool(username.strip() and token.strip())
        self.username = username.strip() if self.authenticated else "Anonymous"
        self.engine.fetcher.set_token(token.strip() if self.authenticated else None)
        self.status_changed.emit("Connected to GitHub" if self.authenticated else "Anonymous access")

    def continue_anonymous(self) -> None:
        self.authenticated = False
        self.username = "Anonymous"
        self.engine.fetcher.set_token(None)
        self.status_changed.emit("Anonymous access · rate limits apply")

    def search_repositories(self, query: str) -> None:
        results = self.engine.handler(query)
        if self.engine.fetcher.last_error:
            self.error_occurred.emit(self.engine.fetcher.last_error)
        if isinstance(results, dict):
            if results:
                self.repository_loaded.emit(results)
            else:
                self.search_finished.emit([])
        else:
            self.search_finished.emit(results)

    def load_repository(self, repository: dict) -> None:
        self.repository_loaded.emit(repository)

    def install_repository(self, repository: dict) -> None:
        """Demo progress only. Replace with the real installer worker."""
        pass
