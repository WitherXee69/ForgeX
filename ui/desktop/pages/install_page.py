from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class InstallPage(QWidget):
    cancel_requested = Signal()

    def __init__(self):
        super().__init__()
        self.repository = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(18)

        self.heading = QLabel("Installation workspace")
        self.heading.setObjectName("PageHeading")
        root.addWidget(self.heading)

        self.status = QLabel("Ready to install")
        self.status.setObjectName("CardHeading")
        root.addWidget(self.status)

        self.stage = QLabel("Waiting for an installation task.")
        self.stage.setObjectName("MutedText")
        root.addWidget(self.stage)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setFormat("%p%")
        root.addWidget(self.progress)

        row = QHBoxLayout()
        row.addStretch(1)
        self.cancel = QPushButton("CANCEL INSTALLATION")
        self.cancel.setObjectName("DangerButton")
        self.cancel.clicked.connect(self.cancel_requested.emit)
        row.addWidget(self.cancel)
        root.addLayout(row)

        logs_title = QLabel("INSTALLATION LOG")
        logs_title.setObjectName("SectionLabel")
        root.addWidget(logs_title)

        self.logs = QTextEdit()
        self.logs.setObjectName("LogConsole")
        self.logs.setReadOnly(True)
        self.logs.setPlaceholderText("Installer output will stream here…")
        root.addWidget(self.logs, 1)

    def begin(self, repo):
        self.repository = repo or {}
        self.heading.setText(
            f"Installing {self.repository.get('name', 'repository')}…"
        )
        self.status.setText("Installation in progress")
        self.progress.setValue(0)
        self.logs.clear()
        self.append_log("Starting installation workflow…")

    def update_progress(self, value, message):
        self.progress.setValue(value)
        self.stage.setText(message)
        self.append_log(f"[{value:03d}%] {message}")

    def append_log(self, message):
        self.logs.append(message)

    def finish(self, success, message):
        self.status.setText(
            "Installation complete" if success else "Installation stopped"
        )
        self.stage.setText(message)
        self.cancel.setEnabled(False)
        self.append_log(message)
