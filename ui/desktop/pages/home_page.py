from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QWidget
)


class HomePage(QWidget):
    action_requested = Signal(str)
    search_requested = Signal(str)

    def __init__(self):
        super().__init__()
        root = QVBoxLayout(self); root.setContentsMargins(28, 24, 28, 24); root.setSpacing(18)
        top = QHBoxLayout(); titles = QVBoxLayout()
        title = QLabel("ForgeX"); title.setObjectName("DashboardTitle")
        subtitle = QLabel("Your Repository Companion"); subtitle.setObjectName("MutedText")
        titles.addWidget(title); titles.addWidget(subtitle); top.addLayout(titles); top.addStretch(1)
        self.welcome = QLabel("Welcome back!"); self.welcome.setObjectName("WelcomeText"); top.addWidget(self.welcome, 0)
        root.addLayout(top)
        search_row = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setObjectName("HomeSearchInput")
        self.search.setMinimumHeight(54)
        self.search.setPlaceholderText("Search repositories… (e.g. NEXA, Minecraft, Tools)")
        self.search.returnPressed.connect(self._submit_search)
        search_row.addWidget(self.search, 1)
        go = QPushButton("SEARCH  →")
        go.setObjectName("HomeSearchButton")
        go.setFixedSize(132, 48)
        go.clicked.connect(self._submit_search)
        search_row.addWidget(go)
        root.addLayout(search_row)
        label = QLabel("QUICK ACTIONS"); label.setObjectName("SectionLabel"); root.addWidget(label)
        grid = QGridLayout(); grid.setSpacing(12)
        actions = [("⚡", "Popular Repositories", "popular"), ("★", "Recently Updated", "recent"), ("◈", "My Library", "library"), ("◎", "Explore More", "search")]
        for i, (icon, text, action) in enumerate(actions):
            button = QPushButton(f"{icon}\n{text}"); button.setObjectName("ActionCard"); button.clicked.connect(lambda checked=False, a=action: self.action_requested.emit(a)); grid.addWidget(button, 0, i)
        root.addLayout(grid)
        activity = QFrame(); activity.setObjectName("Panel")
        av = QVBoxLayout(activity); head = QHBoxLayout(); h = QLabel("Recent Activity"); h.setObjectName("PanelHeading"); head.addWidget(h); head.addStretch(1); view = QPushButton("VIEW ALL  →"); view.setObjectName("TextButton"); head.addWidget(view); av.addLayout(head)
        for line in ["●   Installed: NEXA Shell     ·     2h ago", "●   Viewed: Minecraft Mod Loader     ·     3h ago", "●   Checked: Project Nymora     ·     1d ago"]:
            item = QLabel(line); item.setObjectName("ActivityLine"); av.addWidget(item)
        root.addWidget(activity); root.addStretch(1)

    def _submit_search(self):
        query = self.search.text().strip()
        if query:
            self.search_requested.emit(query)
