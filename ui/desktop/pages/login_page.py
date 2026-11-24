from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QMessageBox,
    QPushButton, QVBoxLayout, QWidget
)


class LoginPage(QWidget):
    login_requested = Signal(str, str)
    anonymous_requested = Signal()

    def __init__(self):
        super().__init__()

        root = QHBoxLayout(self)
        root.setContentsMargins(34, 28, 34, 28)
        root.setSpacing(28)

        hero = QFrame()
        hero.setObjectName("LoginHero")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(36, 30, 36, 28)
        hero_layout.addStretch(1)

        mark = QLabel("F╳")
        mark.setObjectName("HeroMark")
        mark.setAlignment(Qt.AlignCenter)

        name = QLabel("ForgeX")
        name.setObjectName("HeroName")
        name.setAlignment(Qt.AlignCenter)

        tagline = QLabel("AUTOMATED REPOSITORY INSTALLER")
        tagline.setObjectName("HeroTagline")
        tagline.setAlignment(Qt.AlignCenter)

        sub = QLabel("Discover  •  Select  •  Install")
        sub.setObjectName("HeroSub")
        sub.setAlignment(Qt.AlignCenter)

        quote = QLabel("“Build. Install. Evolve.”")
        quote.setObjectName("HeroQuote")

        hero_layout.addWidget(mark)
        hero_layout.addWidget(name)
        hero_layout.addWidget(tagline)
        hero_layout.addWidget(sub)
        hero_layout.addStretch(2)
        hero_layout.addWidget(quote)

        panel_wrap = QWidget()
        panel_wrap.setObjectName("LoginPanelWrap")
        panel = QFrame()
        panel.setObjectName("LoginPanel")

        form = QVBoxLayout(panel)
        form.setContentsMargins(34, 34, 34, 30)
        form.setSpacing(15)

        heading = QLabel("Welcome back!")
        heading.setObjectName("PageHeading")
        caption = QLabel("Sign in to continue")
        caption.setObjectName("MutedText")

        self.username = QLineEdit()
        self.username.setPlaceholderText("GitHub username")
        self.token = QLineEdit()
        self.token.setPlaceholderText("Personal access token")
        self.token.setEchoMode(QLineEdit.Password)

        self.remember = QCheckBox("Remember session on this device")

        login = QPushButton("LOGIN   →")
        login.setObjectName("PrimaryButton")
        login.setMinimumHeight(48)
        login.clicked.connect(self._login)

        divider = QLabel("OR CONTINUE WITHOUT AN ACCOUNT")
        divider.setObjectName("DividerLabel")
        divider.setAlignment(Qt.AlignCenter)

        anonymous = QPushButton("CONTINUE ANONYMOUSLY")
        anonymous.setObjectName("SecondaryButton")
        anonymous.setMinimumHeight(46)
        anonymous.clicked.connect(self._anonymous)

        note = QLabel(
            "Public repositories remain available without signing in. "
            "GitHub applies stricter rate limits to anonymous requests."
        )
        note.setObjectName("HintText")
        note.setWordWrap(True)

        form.addWidget(heading)
        form.addWidget(caption)
        form.addSpacing(12)
        form.addWidget(self.username)
        form.addWidget(self.token)
        form.addWidget(self.remember)
        form.addSpacing(8)
        form.addWidget(login)
        form.addWidget(divider)
        form.addWidget(anonymous)
        form.addWidget(note)
        form.addStretch(1)

        panel_layout = QVBoxLayout(panel_wrap)
        panel_layout.addStretch(1)
        panel_layout.addWidget(panel)
        panel_layout.addStretch(1)

        root.addWidget(hero, 1)
        root.addWidget(panel_wrap, 1)

    def _login(self):
        username = self.username.text().strip()
        token = self.token.text().strip()

        if not username or not token:
            QMessageBox.warning(
                self,
                "Credentials required",
                "Enter both your GitHub username and token, "
                "or continue anonymously."
            )
            return

        self.login_requested.emit(username, token)

    def _anonymous(self):
        dialog = QMessageBox(self)
        dialog.setIcon(QMessageBox.Warning)
        dialog.setWindowTitle("Continue without GitHub?")
        dialog.setText(
            "ForgeX can still search public repositories, but "
            "unauthenticated requests have stricter API limits "
            "and may be temporarily restricted."
        )
        dialog.setInformativeText(
            "You can connect your GitHub account later."
        )

        continue_button = dialog.addButton(
            "Continue", QMessageBox.AcceptRole
        )
        back_button = dialog.addButton(
            "Go Back", QMessageBox.RejectRole
        )
        dialog.setDefaultButton(back_button)
        dialog.exec()

        if dialog.clickedButton() == continue_button:
            self.anonymous_requested.emit()
