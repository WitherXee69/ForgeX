from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QTabWidget, QTextBrowser, QVBoxLayout, QWidget)


class RepositoryPage(QWidget):
    install_requested = Signal(dict)

    def __init__(self):
        super().__init__()
        self.repository = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 22, 24, 22)
        root.setSpacing(16)

        header = QHBoxLayout()
        self.name = QLabel("Repository details")
        self.name.setObjectName("PageHeading")
        header.addWidget(self.name)
        header.addStretch(1)

        self.install = QPushButton("INSTALL REPOSITORY  ▶")
        self.install.setObjectName("PrimaryButton")
        self.install.clicked.connect(
            lambda: self.install_requested.emit(self.repository)
        )
        header.addWidget(self.install)
        root.addLayout(header)

        self.description = QLabel(
            "Select a repository from Search to view its details."
        )
        self.description.setObjectName("MutedText")
        self.description.setWordWrap(True)
        root.addWidget(self.description)

        stats = QHBoxLayout()
        self.stats = QLabel("★ —     Forks —     Language —     License —     Updated —")
        self.stats.setObjectName("MetadataText")
        stats.addWidget(self.stats)
        root.addLayout(stats)

        self.tabs = QTabWidget()
        self.tabs.setObjectName("DetailsTabs")

        self.readme = QTextBrowser()
        self.readme.setObjectName("ReadmeView")
        self.readme.setPlainText(
            "README content will be loaded by the backend."
        )

        self.files = QTextBrowser()
        self.files.setObjectName("ReadmeView")
        self.files.setPlainText("Repository file tree will appear here.")

        self.versions = QTextBrowser()
        self.versions.setObjectName("ReadmeView")
        self.versions.setPlainText(
            "Release and version information will appear here."
        )

        self.dependencies = QTextBrowser()
        self.dependencies.setObjectName("ReadmeView")
        self.dependencies.setPlainText("Recipe dependencies will appear here.")

        tabs = [
            ("README", self.readme),
            ("Files", self.files),
            ("Versions", self.versions),
            ("Dependencies", self.dependencies),
        ]
        for label, widget in tabs:
            self.tabs.addTab(widget, label)

        root.addWidget(self.tabs, 1)

    def set_repository(self, repo, repo_readme):
        self.repository = repo or {}
        self.name.setText(
            self.repository.get("name", "Repository details")
        )
        self.description.setText(
            self.repository.get("description", "No description provided.")
        )
        self.stats.setText(
            f"★ {self.repository.get('stars', 0)}"
            f"     Forks {self.repository.get('forks', 0)}"
            f"     Language {self.repository.get('language', 'Unknown')}"
            f"     License {self.repository.get('license', 'Unknown')}"
            f"     Updated {self.repository.get('updated', '—')}"
        )
        self.readme.setMarkdown(repo_readme if isinstance(repo_readme, str) else "")
        #print(repo_readme)
