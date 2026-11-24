from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget


class TitleBar(QWidget):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self._drag_pos = QPoint()
        self.setObjectName("TitleBar")
        self.setFixedHeight(38)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 8, 0)
        layout.setSpacing(8)
        self.title = QLabel("◈  ForgeX  v1.0.0")
        self.title.setObjectName("WindowTitle")
        layout.addWidget(self.title)
        layout.addStretch(1)
        self.max_button = None
        for label, name, callback in [
            ("−", "MinButton", self.window.showMinimized),
            ("▢", "MaxButton", self.toggle_maximize),
            ("×", "CloseButton", self.window.close),
        ]:
            button = QPushButton(label)
            button.setObjectName(name)
            button.setFixedSize(34, 28)
            button.clicked.connect(callback)
            layout.addWidget(button)
            if name == "MaxButton":
                self.max_button = button

    def toggle_maximize(self):
        if self.window.isMaximized():
            self.window.showNormal()
            self._set_maximize_icon(False)
        else:
            self.window.showMaximized()
            self._set_maximize_icon(True)

    def _set_maximize_icon(self, maximized):
        self.max_button.setText("❐" if maximized else "▢")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and not self.window.isMaximized():
            self.window.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
