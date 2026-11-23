"""ForgeX entry point.

All core service instances are created here and injected into the UI.
"""
from core.context import Context
from core.engine import Engine
from core.handlers.exceptions.exceptions import FX_ExceptionHandler
from core.handlers.repo.fetcher import Fetcher
from config.settings import Settings
from ui.app import ForgeXApp


def main() -> None:
    settings = Settings()
    context = Context()
    exception_handler = FX_ExceptionHandler()
    fetcher = Fetcher(settings, exception_handler)

    # Engine instances are created through this injected factory so the UI
    # never imports or constructs core classes itself.
    engine_factory = lambda query: Engine(query, context, fetcher)

    app = ForgeXApp(
        settings=settings,
        context=context,
        fetcher=fetcher,
        engine_factory=engine_factory,
    )
    app.run()


if __name__ == "__main__":
    main()
