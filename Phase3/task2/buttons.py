import sys
from PySide6.QtCore import QTimer, Signal
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QHBoxLayout,QPushButton,QWidget

class Buttons(QWidget):
    start = Signal()
    pause = Signal()
    reset = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:

        super().__init__(parent)

        self._start_button = QPushButton('Start')
        self._reset_button = QPushButton('Reset')

        layout = QHBoxLayout(self)
        layout.addWidget(self._start_button)
        layout.addWidget(self._reset_button)

        self.timer_paused = True

        self._start_button.clicked.connect(self._b1_clicked)
        self._reset_button.clicked.connect(self._b2_clicked)



    @property
    def timer_paused(self) -> bool:
        return self._timer_paused

    @timer_paused.setter
    def timer_paused(self,state:bool):
        self._timer_paused = state

        if self._timer_paused ==  True:
            self._start_button.setText('Start')
        else:
            self._start_button.setText('Pause')


    def _b1_clicked(self):

        if self.timer_paused == True:
            self.start.emit()
        else:
            self.pause.emit()

    def _b2_clicked(self):
        self.reset.emit()

