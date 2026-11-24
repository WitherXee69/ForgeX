from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QFileDialog, QFrame, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QStackedWidget, QVBoxLayout, QWidget
)


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(34, 30, 34, 30)
        root.setSpacing(18)

        title = QLabel("Settings")
        title.setObjectName("PageHeading")
        subtitle = QLabel("Configure ForgeX to fit the way you work.")
        subtitle.setObjectName("PageSubtitle")
        root.addWidget(title)
        root.addWidget(subtitle)

        body = QHBoxLayout()
        body.setSpacing(18)

        self.navigation = QListWidget()
        self.navigation.setObjectName("SettingsNavigation")
        self.navigation.setFixedWidth(220)
        for icon, label in [
            ("⚙", "General"), ("◈", "Appearance"), ("◎", "Network"),
            ("⟳", "Updates"), ("ⓘ", "About")
        ]:
            self.navigation.addItem(QListWidgetItem(f"{icon}    {label}"))
        body.addWidget(self.navigation)

        self.tabs = QStackedWidget()
        self.tabs.setObjectName("SettingsStack")
        self.tabs.addWidget(self._general_page())
        self.tabs.addWidget(self._appearance_page())
        self.tabs.addWidget(self._network_page())
        self.tabs.addWidget(self._updates_page())
        self.tabs.addWidget(self._about_page())
        body.addWidget(self.tabs, 1)

        brand = QFrame()
        brand.setObjectName("SettingsBrandPanel")
        brand.setFixedWidth(230)
        bv = QVBoxLayout(brand)
        bv.setContentsMargins(20, 24, 20, 24)
        bv.addStretch(1)
        logo = QLabel("F╳")
        logo.setObjectName("SettingsBrandMark")
        logo.setAlignment(Qt.AlignCenter)
        name = QLabel("ForgeX")
        name.setObjectName("SettingsBrandName")
        name.setAlignment(Qt.AlignCenter)
        version = QLabel("VERSION  1.0.0")
        version.setObjectName("SectionLabel")
        version.setAlignment(Qt.AlignCenter)
        by = QLabel("Build. Install. Evolve.\n\nBy WitherXee69")
        by.setObjectName("MutedText")
        by.setAlignment(Qt.AlignCenter)
        bv.addWidget(logo)
        bv.addWidget(name)
        bv.addSpacing(12)
        bv.addWidget(version)
        bv.addSpacing(22)
        bv.addWidget(by)
        bv.addStretch(1)
        body.addWidget(brand)

        root.addLayout(body, 1)
        self.navigation.currentRowChanged.connect(self.tabs.setCurrentIndex)
        self.navigation.setCurrentRow(0)

    def _section(self, heading, description):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(10)
        title = QLabel(heading)
        title.setObjectName("PanelHeading")
        subtitle = QLabel(description)
        subtitle.setObjectName("MutedText")
        subtitle.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(14)
        return page, layout

    def _general_page(self):
        page, layout = self._section("General settings", "Manage ForgeX startup behaviour and installation preferences.")
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        form.setHorizontalSpacing(28)
        form.setVerticalSpacing(24)

        self.auto_update = QCheckBox("Check for updates when ForgeX starts")
        self.auto_update.setChecked(True)
        self.install_dir = QLineEdit("~/ForgeX/Installs")
        self.install_dir.setMinimumHeight(44)
        browse = QPushButton("BROWSE")
        browse.setObjectName("SecondaryButton")
        browse.setMinimumHeight(44)
        browse.clicked.connect(self._browse_directory)
        directory_row = QHBoxLayout()
        directory_row.addWidget(self.install_dir, 1)
        directory_row.addWidget(browse)

        form.addRow("Startup", self.auto_update)
        form.addRow("Install directory", directory_row)
        layout.addLayout(form)
        layout.addStretch(1)
        return page

    def _appearance_page(self):
        page, layout = self._section("Appearance", "Tune the visual presentation of your ForgeX workspace.")
        form = QFormLayout()
        form.setVerticalSpacing(24)
        self.theme = QComboBox()
        self.theme.addItems(["Cyber Violet", "Midnight Blue", "High Contrast"])
        self.theme.setMinimumHeight(44)
        motion = QCheckBox("Enable subtle interface animations")
        motion.setChecked(True)
        form.addRow("Color theme", self.theme)
        form.addRow("Motion", motion)
        layout.addLayout(form)
        layout.addStretch(1)
        return page

    def _network_page(self):
        page, layout = self._section("Network", "GitHub connectivity and request behaviour.")
        form = QFormLayout()
        form.setVerticalSpacing(24)
        api = QLabel("https://api.github.com")
        api.setObjectName("InfoValue")
        timeout = QLabel("Controlled by the backend")
        timeout.setObjectName("InfoValue")
        form.addRow("GitHub API endpoint", api)
        form.addRow("Request timeout", timeout)
        layout.addLayout(form)
        layout.addStretch(1)
        return page

    def _updates_page(self):
        page, layout = self._section("Updates", "Choose how ForgeX checks for new releases.")
        status = QFrame()
        status.setObjectName("InfoInset")
        sv = QVBoxLayout(status)
        heading = QLabel("RELEASE CHANNEL")
        heading.setObjectName("SectionLabel")
        value = QLabel("Stable releases")
        value.setObjectName("InfoValue")
        note = QLabel("Update checks will be connected to the ForgeX update service.")
        note.setObjectName("MutedText")
        note.setWordWrap(True)
        sv.addWidget(heading)
        sv.addWidget(value)
        sv.addWidget(note)
        layout.addWidget(status)
        layout.addStretch(1)
        return page

    def _about_page(self):
        page, layout = self._section("About ForgeX", "A companion for discovering and installing GitHub repositories.")
        card = QFrame()
        card.setObjectName("InfoInset")
        cv = QVBoxLayout(card)
        name = QLabel("ForgeX  v1.0.0")
        name.setObjectName("DetailTitle")
        desc = QLabel("Build. Install. Evolve.\n\nCreated by WitherXee69.")
        desc.setObjectName("InfoValue")
        desc.setWordWrap(True)
        cv.addWidget(name)
        cv.addWidget(desc)
        layout.addWidget(card)
        layout.addStretch(1)
        return page

    def _browse_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Choose installation directory", self.install_dir.text()
        )
        if directory:
            self.install_dir.setText(directory)
