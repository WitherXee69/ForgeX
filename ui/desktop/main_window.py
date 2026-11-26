from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QMessageBox,
    QMainWindow, QStackedWidget, QVBoxLayout, QWidget
)

from .pages.login_page import LoginPage
from .pages.home_page import HomePage
from .pages.search_page import SearchPage
from .pages.repository_page import RepositoryPage
from .pages.install_page import InstallPage
from .pages.settings_page import SettingsPage
from .widgets.title_bar import TitleBar


class MainWindow(QMainWindow):
    def __init__(self, backend):
        super().__init__()
        self.setWindowTitle("ForgeX v1.0.0")
        self.resize(1440, 900)
        self.setMinimumSize(1120, 740)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        self.backend = backend
        self.current_repository = {}

        root = QWidget()
        root.setObjectName("AppRoot")
        outer = QVBoxLayout(root)
        outer.setContentsMargins(1, 1, 1, 1)
        outer.setSpacing(0)

        self.title_bar = TitleBar(self)
        outer.addWidget(self.title_bar)

        self.stack = QStackedWidget()
        self.stack.setObjectName("PageStack")
        outer.addWidget(self.stack, 1)
        self.setCentralWidget(root)

        self.login_page = LoginPage()
        self.home_page = HomePage()
        self.search_page = SearchPage()
        self.repository_page = RepositoryPage()
        self.install_page = InstallPage()
        self.settings_page = SettingsPage()

        self._shell = self._build_shell()
        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self._shell)
        self.stack.setCurrentWidget(self.login_page)

        self.login_page.login_requested.connect(self._login)
        self.login_page.anonymous_requested.connect(self._anonymous)
        self.home_page.action_requested.connect(self._home_action)
        self.home_page.search_requested.connect(self._home_search)
        self.search_page.search_requested.connect(self.backend.search_repositories)
        self.backend.search_finished.connect(self._search_results)
        self.backend.repository_loaded.connect(self._open_repository)
        self.backend.error_occurred.connect(self._show_error)
        self.search_page.repository_selected.connect(self._open_repository)
        self.repository_page.install_requested.connect(self._start_install)
        self.backend.install_progress.connect(self.install_page.update_progress)
        self.backend.install_finished.connect(self.install_page.finish)
        self.install_page.cancel_requested.connect(self._cancel_install)
        self.backend.status_changed.connect(self._set_status)

    def _build_shell(self):
        shell = QWidget()
        layout = QHBoxLayout(shell)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setMinimumWidth(238)
        sidebar.setMaximumWidth(270)
        sv = QVBoxLayout(sidebar)
        sv.setContentsMargins(18, 22, 18, 20)
        sv.setSpacing(10)

        logo = QLabel("F╳")
        logo.setObjectName("SidebarLogo")
        logo.setAlignment(Qt.AlignCenter)
        sv.addWidget(logo)

        brand = QLabel("ForgeX")
        brand.setObjectName("SidebarBrand")
        brand.setAlignment(Qt.AlignCenter)
        sv.addWidget(brand)

        tagline = QLabel("REPOSITORY COMPANION")
        tagline.setObjectName("SidebarTagline")
        tagline.setAlignment(Qt.AlignCenter)
        sv.addWidget(tagline)
        sv.addSpacing(18)

        self.nav = QListWidget()
        self.nav.setObjectName("NavigationList")
        for label, page in [
            ("⌂    Home", "home"),
            ("⌕    Discover", "search"),
            ("◈    My Library", "library"),
            ("⚙    Settings", "settings"),
            ("ⓘ    About", "about"),
        ]:
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, page)
            self.nav.addItem(item)
        self.nav.currentRowChanged.connect(self._navigate)
        sv.addWidget(self.nav, 1)

        footer = QFrame()
        footer.setObjectName("SidebarFooterPanel")
        fv = QVBoxLayout(footer)
        fv.setContentsMargins(12, 12, 12, 12)
        version = QLabel("FORGEX  •  v1.0.0")
        version.setObjectName("SidebarVersion")
        author = QLabel("Crafted by WitherXee69")
        author.setObjectName("SidebarFooter")
        fv.addWidget(version)
        fv.addWidget(author)
        sv.addWidget(footer)

        content = QWidget()
        content.setObjectName("MainContent")
        cv = QVBoxLayout(content)
        cv.setContentsMargins(0, 0, 0, 0)
        cv.setSpacing(0)

        self.connection = QLabel("●  Waiting for connection")
        self.connection.setObjectName("ConnectionBar")
        cv.addWidget(self.connection)

        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("ContentStack")
        for page in [
            self.home_page, self.search_page, self.repository_page,
            self.install_page, self.settings_page
        ]:
            self.content_stack.addWidget(page)
        cv.addWidget(self.content_stack, 1)

        layout.addWidget(sidebar)
        layout.addWidget(content, 1)
        self._shell = shell
        return shell

    def _login(self, username, token):
        self.backend.login(username, token)
        self._enter_app()

    def _anonymous(self):
        self.backend.continue_anonymous()
        self._enter_app()

    def _enter_app(self):
        self.stack.setCurrentWidget(self._shell)
        self.nav.setCurrentRow(0)
        self.home_page.welcome.setText(
            f"Welcome back, {self.backend.username}!"
        )

    def _set_status(self, text):
        self.connection.setText("●  " + text)

    def _navigate(self, row):
        if row == 0:
            self.content_stack.setCurrentWidget(self.home_page)
        elif row == 1:
            self.content_stack.setCurrentWidget(self.search_page)
        elif row == 2:
            self.content_stack.setCurrentWidget(self.search_page)
        elif row == 3:
            self.content_stack.setCurrentWidget(self.settings_page)
            self.settings_page.tabs.setCurrentIndex(0)
        elif row == 4:
            self.content_stack.setCurrentWidget(self.settings_page)
            self.settings_page.tabs.setCurrentIndex(4)

    def _home_action(self, action):
        if action == "settings":
            self.nav.setCurrentRow(3)
        else:
            self.nav.setCurrentRow(1)
            if action in ("popular", "recent", "library"):
                self.search_page.query.setText("")
            self.search_page._search()

    def _home_search(self, query):
        self.search_page.query.setText(query)
        self.nav.setCurrentRow(1)
        self.search_page._search()

    def _search_results(self, repositories):
        self.search_page.set_results(repositories)
        self.content_stack.setCurrentWidget(self.search_page)

    def _show_error(self, message):
        for tag in ("[red]", "[/red]", "[green]", "[/green]"):
            message = message.replace(tag, "")
        QMessageBox.warning(self, "GitHub request failed", message)

    def _open_repository(self, repository):
        self.current_repository = repository
        self.readme = self.backend.load_repository(repository)
        self.repository_page.set_repository(repository, self.readme)
        self.content_stack.setCurrentWidget(self.repository_page)

    def _start_install(self, repository):
        self.current_repository = repository
        self.install_page.begin(repository)
        self.content_stack.setCurrentWidget(self.install_page)
        self.backend.install_repository(repository)

    def _cancel_install(self):
        timer = self.backend._demo_install_timer
        if timer:
            timer.stop()
        self.install_page.finish(False, "Installation cancelled by user.")
