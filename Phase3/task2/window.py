from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from buttons import Buttons
from stack import Stack


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        self.stack = Stack(self)
        self.buttons = Buttons(self)

        self.setWindowTitle('Main Window')
        self.resize(500,400)

        central_widget = QWidget()

        layout = QVBoxLayout()

        layout.addWidget(self.stack)
        layout.addWidget(self.buttons)

        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        self.buttons.start.connect(self.stack.start_counter)
        self.buttons.pause.connect(self.stack.pause)
        self.buttons.reset.connect(self.stack.reset)

        self.stack.time_stopped.connect(self._switch_buttons)

    def _switch_buttons(self,state:bool) -> None:

        self.buttons.timer_paused = state



        