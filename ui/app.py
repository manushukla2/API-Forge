import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget,
                              QHBoxLayout, QVBoxLayout, QStackedWidget)
from PyQt6.QtCore import Qt
from ui.theme import STYLESHEET, COLORS
from ui.router import Router
from ui.components.sidebar import Sidebar
from ui.components.topbar import TopBar
from ui.components.toast import Toast

from ui.screens.home import HomeScreen
from ui.screens.input_selector import InputSelector
from ui.screens.qa.qa_home import QAHomeScreen
from ui.screens.qa.doc_input import DocInputScreen
from ui.screens.qa.flow_screen import FlowScreen
from ui.screens.qa.scenario_screen import ScenarioScreen
from ui.screens.qa.test_runner import TestRunnerScreen
from ui.screens.qa.evidence_screen import EvidenceScreen
from ui.screens.qa.report_screen import ReportScreen
from ui.screens.dev.dev_home import DevHomeScreen
from ui.screens.dev.requirement_input import RequirementInputScreen
from ui.screens.dev.stack_screen import StackScreen
from ui.screens.dev.architecture_screen import ArchitectureScreen
from ui.screens.dev.schema_screen import SchemaScreen
from ui.screens.dev.export_screen import ExportScreen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("APIForge v0.1.0")
        self.setMinimumSize(1200, 750)
        self._build()

    def _build(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.navigate.connect(self._navigate)
        root.addWidget(self.sidebar)

        # Right side
        right = QVBoxLayout()
        right.setContentsMargins(0, 0, 0, 0)
        right.setSpacing(0)

        self.topbar = TopBar()
        self.topbar.settings_clicked.connect(lambda: self.toast.info("Settings coming soon"))
        right.addWidget(self.topbar)

        # Stack
        self.stack = QStackedWidget()
        right.addWidget(self.stack)

        right_widget = QWidget()
        right_widget.setLayout(right)
        root.addWidget(right_widget)

        # Toast
        self.toast = Toast(self)
        self.toast.setFixedWidth(320)

        # Init router
        self.router = Router(self.stack)

        # Register screens
        self.home_screen        = HomeScreen()
        self.qa_home            = QAHomeScreen()
        self.doc_input          = DocInputScreen()
        self.flow_screen        = FlowScreen()
        self.scenario_screen    = ScenarioScreen()
        self.test_runner        = TestRunnerScreen()
        self.evidence_screen    = EvidenceScreen()
        self.report_screen      = ReportScreen()
        self.dev_home           = DevHomeScreen()
        self.req_input          = RequirementInputScreen()
        self.stack_screen       = StackScreen()
        self.arch_screen        = ArchitectureScreen()
        self.schema_screen      = SchemaScreen()
        self.export_screen      = ExportScreen()

        self.router.register("home",               self.home_screen)
        self.router.register("qa_home",            self.qa_home)
        self.router.register("doc_input",          self.doc_input)
        self.router.register("flow_screen",        self.flow_screen)
        self.router.register("scenario_screen",    self.scenario_screen)
        self.router.register("test_runner",        self.test_runner)
        self.router.register("evidence_screen",    self.evidence_screen)
        self.router.register("report_screen",      self.report_screen)
        self.router.register("dev_home",           self.dev_home)
        self.router.register("requirement_input",  self.req_input)
        self.router.register("stack_screen",       self.stack_screen)
        self.router.register("architecture_screen",self.arch_screen)
        self.router.register("schema_screen",      self.schema_screen)
        self.router.register("export_screen",      self.export_screen)

        # Wire signals
        self.home_screen.navigate.connect(self._navigate)
        self.qa_home.navigate.connect(self._navigate)
        self.dev_home.navigate.connect(self._navigate)
        self.doc_input.start_testing.connect(self._start_testing)
        self.test_runner.testing_done.connect(self._on_testing_done)
        self.req_input.studio_done.connect(self._on_studio_done)

        # Start on home
        self.router.navigate("home")
        self.sidebar.set_active("home")
        self.topbar.set_title("Home")
        self.topbar.set_status("● Ready", COLORS["success"])

    def _navigate(self, route: str):
        self.router.navigate(route)
        self.sidebar.set_active(route)
        self.topbar.set_title(route.replace("_", " ").title())

    def _start_testing(self, source: str, auth: dict):
        self.test_runner.set_source(source, auth)
        self._navigate("test_runner")
        self.test_runner._start()

    def _on_testing_done(self, result: dict):
        flow_data = result.get("flow", {})
        self.flow_screen.load(flow_data)
        self.evidence_screen.load(result.get("evidence", []))
        self.report_screen.load(result)
        self.qa_home.refresh()
        self.toast.success("Testing complete! Check Evidence & Report.")
        self.topbar.set_status("● Tests Complete", COLORS["success"])

    def _on_studio_done(self, result: dict):
        self.stack_screen.load(result)
        self.arch_screen.load(result)
        self.schema_screen.load(result)
        self.export_screen.load(result)
        self._navigate("stack_screen")
        self.toast.success("Analysis complete!")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.toast.move(self.width() - 340, self.height() - 64)
