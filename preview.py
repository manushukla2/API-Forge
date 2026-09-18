import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QStackedWidget
from PyQt6.QtCore import Qt
from ui.theme import STYLESHEET, COLORS, FONTS
from ui.components.sidebar import Sidebar
from ui.components.topbar import TopBar
from ui.components.progress_bar import ProgressWidget
from ui.components.toast import Toast


class PreviewWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("APIForge v0.1.0")
        self.setMinimumSize(1100, 700)

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        root.addWidget(self.sidebar)

        # Right side
        right = QVBoxLayout()
        right.setContentsMargins(0, 0, 0, 0)
        right.setSpacing(0)

        # Topbar
        self.topbar = TopBar()
        right.addWidget(self.topbar)

        # Main content
        self.stack = QStackedWidget()

        # Home placeholder
        home = QWidget()
        home.setStyleSheet(f"background-color: {COLORS['bg_primary']};")
        hl = QVBoxLayout(home)
        hl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("⚡ Welcome to APIForge")
        title.setObjectName("heading")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"font-size: 28px; font-weight: 700; color: {COLORS['text_primary']};")

        sub = QLabel("Test & Build AI-powered APIs — drop your docs and go")
        sub.setObjectName("subheading")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub.setStyleSheet(f"font-size: 14px; color: {COLORS['text_secondary']}; margin-top: 8px;")

        hl.addWidget(title)
        hl.addWidget(sub)

        # Progress bar preview
        prog = ProgressWidget()
        prog.setFixedWidth(400)
        prog.update("All systems ready", 100)
        hl.addSpacing(24)
        hl.addWidget(prog, alignment=Qt.AlignmentFlag.AlignCenter)

        self.stack.addWidget(home)
        right.addWidget(self.stack)

        # Toast
        self.toast = Toast(self)
        self.toast.setFixedWidth(300)

        root.addLayout(right)

        # Sidebar navigation
        self.sidebar.navigate.connect(self._on_navigate)
        self.sidebar.set_active("home")
        self.topbar.set_status("● Ready", COLORS["success"])

    def _on_navigate(self, route: str):
        self.topbar.set_title(route.replace("_", " ").title())
        self.toast.info(f"Navigated to {route}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.toast.move(self.width() - 320, self.height() - 60)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    win = PreviewWindow()
    win.show()
    sys.exit(app.exec())
