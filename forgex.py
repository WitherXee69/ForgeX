"""ForgeX entry point.

All core service instances are created here and injected into the UI.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from core.context import Context
from core.engine import Engine
from core.handlers.exceptions.exceptions import FX_ExceptionHandler
from core.handlers.repo.fetcher import Fetcher

from config.settings import Settings

from ui.desktop.controller.forgeController import ForgeXController

from ui.desktop.main_window import MainWindow


def main() -> int:
    settings = Settings()
    context = Context()
    exception_handler = FX_ExceptionHandler()
    fetcher = Fetcher(settings, exception_handler)

    engine = Engine(context, fetcher)

    fxController = ForgeXController(engine=engine, context=context)

    # Engine instances are created through this injected factory so the UI
    # never imports or constructs core classes itself.
    #engine_factory = lambda query: Engine(query, context, fetcher)

    # Let Qt scale naturally on high-DPI and Windows display scaling.
    app = QApplication(sys.argv)
    app.setApplicationName("ForgeX")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Withering Studios")
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 11))

    stylesheet = Path("ui\\desktop\\styles\\theme.qss")
    if stylesheet.exists():
        app.setStyleSheet(stylesheet.read_text(encoding="utf-8"))

    window = MainWindow(fxController)
    window.show()
    return app.exec()


if __name__ == "__main__":
    main()
