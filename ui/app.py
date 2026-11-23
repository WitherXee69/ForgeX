"""Textual interface for ForgeX.

The UI receives its dependencies from forgex.py. It does not construct core
services or contain GitHub API logic.
"""
from __future__ import annotations

import webbrowser
from typing import Any

from textual import work
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Input, Label, Static


class LoginScreen(Screen):
    """GitHub credential screen."""

    BINDINGS = [("escape", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Container(
            Horizontal(
                Vertical(
                    Static("F X", id="login-mark"),
                    Static("ForgeX", id="login-brand"),
                    Static("AUTOMATED REPOSITORY INSTALLER", classes="eyebrow"),
                    Static("Discover  •  Select  •  Install", classes="muted"),
                    id="login-brand-panel",
                ),
                Vertical(
                    Static("WELCOME BACK", classes="eyebrow"),
                    Static("Connect to GitHub", id="login-heading"),
                    Static("Sign in to start exploring repositories.", classes="muted"),
                    Label("GITHUB USERNAME"),
                    Input(placeholder="your-github-username", id="github-username"),
                    Label("PERSONAL ACCESS TOKEN"),
                    Input(placeholder="ghp_••••••••••••••••", password=True, id="github-token"),
                    Static("Your token stays in this session and is not written to disk.", id="login-note"),
                    Button("CONNECT TO GITHUB  →", id="login-submit", variant="primary"),
                    Static("ForgeX  /  PRIVATE SESSION", classes="eyebrow login-foot"),
                    id="login-card",
                ),
                id="login-layout",
            ),
            id="login-shell",
        )

    def on_mount(self) -> None:
        self.query_one("#github-username", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "login-submit":
            return

        username = self.query_one("#github-username", Input).value.strip()
        token = self.query_one("#github-token", Input).value.strip()
        if not username or not token:
            self.notify("Enter both your GitHub username and token.", severity="warning")
            return

        app = self.app
        app.settings.git_username = username
        app.settings.git_token = token
        app.fetcher.headers["Authorization"] = f"token {token}"
        self.app.pop_screen()
        self.app.push_screen(DashboardScreen())


class DashboardScreen(Screen):
    """Repository search and details dashboard."""

    def __init__(self) -> None:
        super().__init__()
        self.repositories: list[dict[str, Any]] = []
        self.selected_repo: dict[str, Any] | None = None

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Vertical(
                Static("F X", id="sidebar-logo"),
                Static("FORGEX", id="sidebar-name"),
                Static("WORKSPACE", classes="eyebrow sidebar-label"),
                Button("⌂   Home", id="nav-home", variant="primary"),
                Button("⌕   Search", id="nav-search"),
                Static(""),
                Static("SYSTEM", classes="eyebrow sidebar-label"),
                Static("●  GITHUB CONNECTED", id="connection-state"),
                Static("v1.0.0  •  WITHERXEE69", id="sidebar-version"),
                id="sidebar",
            ),
            Vertical(
                Horizontal(
                    Vertical(
                        Static("REPOSITORY COMPANION", classes="eyebrow"),
                        Static("Discover something.", id="welcome-title"),
                    ),
                    Static("● ONLINE", id="online-indicator"),
                    id="topbar",
                ),
                Horizontal(
                    Input(
                        placeholder="Search repositories...  (e.g. NEXA, Minecraft, tools)",
                        id="repo-query",
                    ),
                    Button("⌕  SEARCH", id="search-submit", variant="primary"),
                    id="search-row",
                ),
                Horizontal(
                    Button("⚡  POPULAR REPOS", id="quick-popular"),
                    Button("◷  RECENTLY UPDATED", id="quick-recent"),
                    Button("↻  CLEAR", id="clear-results"),
                    id="quick-actions",
                ),
                Horizontal(
                    Vertical(
                        Horizontal(
                            Static("SEARCH RESULTS", classes="section-title"),
                            Static("READY", id="result-count", classes="eyebrow"),
                            id="results-heading",
                        ),
                        DataTable(id="repo-table", cursor_type="row", zebra_stripes=True),
                        id="results-panel",
                    ),
                    Vertical(
                        Horizontal(
                            Static("REPOSITORY OVERVIEW", classes="section-title"),
                            Static("NO SELECTION", id="detail-state", classes="eyebrow"),
                            id="detail-heading",
                        ),
                        Static("◇", id="repo-emblem"),
                        Static("Select a repository", id="repo-title"),
                        Static("Search GitHub or choose a result to inspect its details.", id="repo-description"),
                        Static("★  —       ⑂  —       ◈  —", id="repo-stats"),
                        Static("OWNER / REPOSITORY", classes="eyebrow detail-label"),
                        Static("—", id="repo-full-name"),
                        Static("LANGUAGE", classes="eyebrow detail-label"),
                        Static("—", id="repo-language"),
                        Static("UPDATED", classes="eyebrow detail-label"),
                        Static("—", id="repo-updated"),
                        Static("LICENSE", classes="eyebrow detail-label"),
                        Static("—", id="repo-license"),
                        Button("↗  OPEN ON GITHUB", id="open-github", disabled=True),
                        id="detail-panel",
                    ),
                    id="workspace",
                ),
                Horizontal(
                    Static("◆  FORGEX SYSTEM", id="status-left"),
                    Static("DISCOVER  /  SELECT  /  INSTALL", id="status-right"),
                    id="statusbar",
                ),
                id="main-area",
            ),
            id="dashboard",
        )
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#repo-table", DataTable)
        table.add_columns("REPOSITORY", "★", "LANGUAGE")
        self.query_one("#repo-query", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "repo-query":
            self.start_search(event.value)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "search-submit":
            self.start_search(self.query_one("#repo-query", Input).value)
        elif button_id == "quick-popular":
            query = "stars:>1000"
            self.query_one("#repo-query", Input).value = query
            self.start_search(query)
        elif button_id == "quick-recent":
            query = "sort:updated"
            self.query_one("#repo-query", Input).value = query
            self.start_search(query)
        elif button_id == "clear-results":
            self.clear_results()
        elif button_id == "nav-search":
            self.query_one("#repo-query", Input).focus()
        elif button_id == "nav-home":
            self.clear_results()
        elif button_id == "open-github" and self.selected_repo:
            url = self.selected_repo.get("html_url")
            if url:
                webbrowser.open(url)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        try:
            index = int(event.row_key.value)
            self.show_repository(self.repositories[index])
        except (ValueError, IndexError, TypeError):
            return

    def start_search(self, query: str) -> None:
        query = query.strip()
        if not query:
            self.notify("Enter a repository name, owner/repo, or GitHub URL.", severity="warning")
            return
        self.query_one("#result-count", Static).update("SEARCHING…")
        self.query_one("#status-left", Static).update("◌  CONTACTING GITHUB")
        self.query_one("#search-submit", Button).disabled = True
        self.run_search(query)

    @work(thread=True, exclusive=True)
    def run_search(self, query: str) -> None:
        try:
            result = self.app.engine_factory(query).handler()
        except Exception as exc:  # Keep unexpected network/API errors inside the UI.
            result = {"type": "error", "message": str(exc)}
        self.app.call_from_thread(self.display_search_result, result)

    def display_search_result(self, result: dict[str, Any]) -> None:
        self.query_one("#search-submit", Button).disabled = False
        table = self.query_one("#repo-table", DataTable)
        table.clear()
        self.repositories = []
        kind = result.get("type")

        if kind == "single":
            repo = result.get("data") or {}
            self.repositories = [repo]
            self.add_repository_row(0, repo)
            self.show_repository(repo)
            self.query_one("#result-count", Static).update("1 FOUND")
            self.query_one("#status-left", Static).update("✓  REPOSITORY FETCHED")
        elif kind == "multiple":
            self.repositories = result.get("options") or []
            for index, repo in enumerate(self.repositories):
                self.add_repository_row(index, repo)
            self.query_one("#result-count", Static).update(f"{len(self.repositories)} FOUND")
            self.query_one("#status-left", Static).update("✓  SEARCH COMPLETE")
            if self.repositories:
                self.show_repository(self.repositories[0])
        else:
            message = str(result.get("message", "No repositories found."))
            self.query_one("#result-count", Static).update("NO RESULTS")
            self.query_one("#status-left", Static).update("!  SEARCH FINISHED")
            self.notify(self.clean_message(message), severity="error", timeout=6)

    def add_repository_row(self, index: int, repo: dict[str, Any]) -> None:
        name = str(repo.get("full_name") or repo.get("name") or "Unknown repository")
        stars = repo.get("stargazers_count", 0)
        language = repo.get("language") or "—"
        self.query_one("#repo-table", DataTable).add_row(
            name[:42], self.format_number(stars), str(language)[:18], key=str(index)
        )

    def show_repository(self, repo: dict[str, Any]) -> None:
        self.selected_repo = repo
        self.query_one("#detail-state", Static).update("SELECTED")
        self.query_one("#repo-title", Static).update(str(repo.get("name") or "Unknown repository"))
        self.query_one("#repo-description", Static).update(
            repo.get("description") or "No description provided by the repository owner."
        )
        stars = self.format_number(repo.get("stargazers_count", 0))
        forks = self.format_number(repo.get("forks_count", 0))
        issues = self.format_number(repo.get("open_issues_count", 0))
        self.query_one("#repo-stats", Static).update(f"★  {stars}     ⑂  {forks}     ◈  {issues}")
        self.query_one("#repo-full-name", Static).update(str(repo.get("full_name") or "—"))
        self.query_one("#repo-language", Static).update(str(repo.get("language") or "Not specified"))
        self.query_one("#repo-updated", Static).update(str(repo.get("updated_at") or "Unknown"))
        license_info = repo.get("license") or {}
        self.query_one("#repo-license", Static).update(str(license_info.get("spdx_id") or "Not specified"))
        self.query_one("#open-github", Button).disabled = not bool(repo.get("html_url"))

    def clear_results(self) -> None:
        self.query_one("#repo-table", DataTable).clear()
        self.repositories = []
        self.selected_repo = None
        self.query_one("#result-count", Static).update("READY")
        self.query_one("#detail-state", Static).update("NO SELECTION")
        self.query_one("#repo-title", Static).update("Select a repository")
        self.query_one("#repo-description", Static).update(
            "Search GitHub or choose a result to inspect its details."
        )
        self.query_one("#repo-stats", Static).update("★  —       ⑂  —       ◈  —")
        for widget_id in ("repo-full-name", "repo-language", "repo-updated", "repo-license"):
            self.query_one(f"#{widget_id}", Static).update("—")
        self.query_one("#open-github", Button).disabled = True
        self.query_one("#status-left", Static).update("◆  FORGEX READY")

    @staticmethod
    def format_number(value: Any) -> str:
        try:
            number = int(value or 0)
            return f"{number:,}"
        except (TypeError, ValueError):
            return "0"

    @staticmethod
    def clean_message(message: str) -> str:
        import re
        return re.sub(r"\[/?[^\]]+\]", "", message)


class ForgeXApp(App):
    """Top-level UI. Core objects are injected by forgex.py."""

    TITLE = "ForgeX"
    SUB_TITLE = "Automated Repository Installer"
    CSS_PATH = "theme.tcss"
    ENABLE_COMMAND_PALETTE = False

    def __init__(self, settings: Any, context: Any, fetcher: Any, engine_factory: Any):
        super().__init__()
        self.settings = settings
        self.context = context
        self.fetcher = fetcher
        self.engine_factory = engine_factory

    def on_mount(self) -> None:
        self.push_screen(LoginScreen())
