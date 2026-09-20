import sys
from PySide6.QtCore import QTimer, Signal
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QLabel, QLineEdit, QStackedWidget, QWidget


class Stack(QStackedWidget):
    time_stopped = Signal(bool)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._line_edit = QLineEdit(self)
        self._line_edit.setPlaceholderText("Enter seconds...")
        validator = QIntValidator(1, 3600, self)
        self._line_edit.setValidator(validator)

        
        self._label = QLabel("00:00", self)

        
        self.addWidget(self._line_edit)  
        self.addWidget(self._label)  

        
        self._remaining_seconds = 0
        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._decrement)


    def start_counter(self) -> None:

        if self._remaining_seconds > 0 and self.currentIndex() == 1:
            self._timer.start()
            self.time_stopped.emit(False)
            return

        if self._line_edit.hasAcceptableInput():
            self._remaining_seconds = int(self._line_edit.text())
            self._update_display()

            self.setCurrentIndex(1)

            self._timer.start()
            self.time_stopped.emit(False)

    def _decrement(self) -> None:
        self._remaining_seconds -= 1
        self._update_display()


        if self._remaining_seconds <= 0:
            self.reset()

    def pause(self) -> None:

        self._timer.stop()
        self.time_stopped.emit(True)
        pass

    def reset(self) -> None:

        self._timer.stop()
        self._remaining_seconds = 0
        self._line_edit.clear()
        self.setCurrentIndex(0)
        self.time_stopped.emit(True)


    def _update_display(self) -> None:
        minutes = self._remaining_seconds // 60
        seconds = self._remaining_seconds % 60
        self._label.setText(f"{minutes:02d}:{seconds:02d}")