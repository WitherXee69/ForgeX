from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSplitter, QVBoxLayout, QWidget
)


class SearchPage(QWidget):
    search_requested = Signal(str)
    repository_selected = Signal(dict)

    def __init__(self):
        super().__init__()
        self.repositories = []
        root = QVBoxLayout(self)
        root.setContentsMargins(34, 30, 34, 30)
        root.setSpacing(20)

        header = QVBoxLayout()
        title = QLabel("Discover repositories")
        title.setObjectName("PageHeading")
        subtitle = QLabel("Find a project, inspect its details, and bring it into your environment.")
        subtitle.setObjectName("PageSubtitle")
        header.addWidget(title)
        header.addWidget(subtitle)
        root.addLayout(header)

        search_panel = QFrame()
        search_panel.setObjectName("SearchToolbar")
        row = QHBoxLayout(search_panel)
        row.setContentsMargins(14, 10, 14, 10)
        self.query = QLineEdit()
        self.query.setMinimumHeight(48)
        self.query.setPlaceholderText("Search by repository name, owner, language, or keyword…")
        self.query.returnPressed.connect(self._search)
        row.addWidget(self.query, 1)

        button = QPushButton("⌕   SEARCH")
        button.setObjectName("PrimaryButton")
        button.setMinimumWidth(150)
        button.setMinimumHeight(48)
        button.clicked.connect(self._search)
        row.addWidget(button)
        root.addWidget(search_panel)

        split = QSplitter(Qt.Horizontal)
        split.setObjectName("SearchSplit")
        split.setChildrenCollapsible(False)

        results_panel = QFrame()
        results_panel.setObjectName("Panel")
        left = QVBoxLayout(results_panel)
        left.setContentsMargins(16, 16, 16, 14)
        left.setSpacing(12)
        result_header = QHBoxLayout()
        result_title = QLabel("SEARCH RESULTS")
        result_title.setObjectName("SectionLabel")
        self.result_count = QLabel("Ready to search")
        self.result_count.setObjectName("MutedText")
        result_header.addWidget(result_title)
        result_header.addStretch(1)
        result_header.addWidget(self.result_count)
        left.addLayout(result_header)

        self.results = QListWidget()
        self.results.setObjectName("RepositoryList")
        self.results.setSpacing(6)
        self.results.setWordWrap(True)
        self.results.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.results.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.results.currentRowChanged.connect(self._selection_changed)
        left.addWidget(self.results, 1)
        split.addWidget(results_panel)

        detail = QFrame()
        detail.setObjectName("DetailPanel")
        dv = QVBoxLayout(detail)
        dv.setContentsMargins(28, 26, 28, 24)
        dv.setSpacing(16)

        self.detail_kicker = QLabel("REPOSITORY PREVIEW")
        self.detail_kicker.setObjectName("SectionLabel")
        self.detail_name = QLabel("Choose a repository")
        self.detail_name.setObjectName("DetailTitle")
        self.detail_name.setWordWrap(True)
        self.detail_desc = QLabel("Search results will appear here. Select a project to see its description and repository metadata.")
        self.detail_desc.setObjectName("DetailDescription")
        self.detail_desc.setWordWrap(True)
        self.detail_meta = QLabel("")
        self.detail_meta.setObjectName("MetadataText")
        self.detail_tags = QLabel("")
        self.detail_tags.setObjectName("TagText")
        self.detail_tags.setWordWrap(True)

        info = QFrame()
        info.setObjectName("InfoInset")
        iv = QVBoxLayout(info)
        iv.setContentsMargins(18, 16, 18, 16)
        info_title = QLabel("ABOUT THIS RESULT")
        info_title.setObjectName("SectionLabel")
        self.detail_full_name = QLabel("Repository information will appear here.")
        self.detail_full_name.setObjectName("InfoValue")
        self.detail_language = QLabel("Language  —")
        self.detail_language.setObjectName("InfoValue")
        iv.addWidget(info_title)
        iv.addWidget(self.detail_full_name)
        iv.addWidget(self.detail_language)

        dv.addWidget(self.detail_kicker)
        dv.addWidget(self.detail_name)
        dv.addWidget(self.detail_desc)
        dv.addWidget(self.detail_meta)
        dv.addWidget(self.detail_tags)
        dv.addWidget(info)
        dv.addStretch(1)

        open_button = QPushButton("VIEW REPOSITORY DETAILS   →")
        open_button.setObjectName("PrimaryButton")
        open_button.setMinimumHeight(48)
        open_button.clicked.connect(self._open_selected)
        dv.addWidget(open_button)
        split.addWidget(detail)
        split.setStretchFactor(0, 4)
        split.setStretchFactor(1, 6)
        split.setSizes([520, 760])
        root.addWidget(split, 1)

    def _search(self):
        query = self.query.text().strip()
        if query:
            self.result_count.setText("Searching…")
            self.search_requested.emit(query)

    def set_results(self, repositories):
        self.repositories = repositories or []
        self.results.clear()
        self.result_count.setText(f"{len(self.repositories)} found")
        for repo in self.repositories:
            name = repo.get("name", "Unknown repository")
            owner = repo.get("full_name", "")
            desc = repo.get("description") or "No description provided."
            #item = QListWidgetItem(f"◈   {name}\n      {owner}\n      {desc}")
            item = QListWidgetItem(f"◈   {name}\n      {owner}")
            item.setData(Qt.UserRole, repo)
            self.results.addItem(item)
        if self.repositories:
            self.results.setCurrentRow(0)
        else:
            self.detail_name.setText("No repositories found")
            self.detail_desc.setText("Try a different search term, or check your GitHub connection.")
            self.detail_full_name.setText("No matching repository")
            self.detail_language.setText("Language  —")

    def _selection_changed(self, row):
        if 0 <= row < len(self.repositories):
            repo = self.repositories[row]
            self.detail_name.setText(repo.get("name", "Repository"))
            self.detail_desc.setText(repo.get("description") or "No description provided.")
            self.detail_meta.setText(
                f"★  {repo.get('stars', 0):,}     ⑂  {repo.get('forks', 0):,}     "
                f"License  {repo.get('license', 'Unknown')}"
            )
            self.detail_tags.setText("   •   ".join(repo.get("tags", [])))
            self.detail_full_name.setText(repo.get("full_name", "—"))
            self.detail_language.setText(f"Language  {repo.get('language', 'Unknown')}")

    def _open_selected(self):
        row = self.results.currentRow()
        if 0 <= row < len(self.repositories):
            self.repository_selected.emit(self.repositories[row])
