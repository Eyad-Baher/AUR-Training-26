from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from data import MyData
from input import Input
from status_widget import StatusWidget
from assets import get_asset 

# Update this line inside Window.__init__:


class Window(QMainWindow):

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.data = MyData(self)

        self.status_widget = StatusWidget("clock.qml", self.data, self)


        self.status_widget = StatusWidget("clock.qml", self.data, self)

        self.input_widget = Input(self)

        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.status_widget)  
        layout.addWidget(self.input_widget)
        self.setCentralWidget(central_widget)  

        self.input_widget.time_entered.connect(self._set_time)

        self.setWindowTitle("Clock")
        self.resize(500, 500)



    def _set_time(self, hour: int, min: int, sec: int) -> None:
        self.data.hours = hour
        self.data.mins = min
        self.data.secs = sec