from PyQt6.QtWidgets import QStackedWidget


class Router:
    def __init__(self, stack: QStackedWidget):
        self.stack  = stack
        self.routes = {}
        self.history = []

    def register(self, name: str, widget):
        self.routes[name] = widget
        self.stack.addWidget(widget)

    def navigate(self, name: str):
        if name not in self.routes:
            return
        widget = self.routes[name]
        self.stack.setCurrentWidget(widget)
        self.history.append(name)

    def back(self):
        if len(self.history) > 1:
            self.history.pop()
            prev = self.history[-1]
            self.stack.setCurrentWidget(self.routes[prev])

    def current(self) -> str:
        if self.history:
            return self.history[-1]
        return ""
