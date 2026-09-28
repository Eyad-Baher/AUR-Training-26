from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from task.gui.status_widget import StatusWidget
from task.backend.mediator import Mediator
#import mediator
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(400, 350)
       
        self._mediator = Mediator()

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.status_widget = StatusWidget('battery.qml', self._mediator)
        
        self.emergency_btn = QPushButton(" EMERGENCY STOP ")
        self.emergency_btn.clicked.connect(self._mediator.trigger_emergency)
        #self.emergency_btn.clicked.connect(self._mediator.trigger_emergency)
        self.emergency_btn.setMinimumHeight(50)

        layout.addWidget(self.status_widget)
        layout.addWidget(self.emergency_btn)

        self.setCentralWidget(central_widget)

        self.show()

