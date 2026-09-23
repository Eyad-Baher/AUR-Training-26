from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QWidget,QVBoxLayout


class Input(QWidget):
    time_entered = Signal(int, int, int)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self._hours_input = QLineEdit(self)
        self._hours_input.setPlaceholderText("Hours (0-11)")

        self._min_input = QLineEdit(self)
        self._min_input.setPlaceholderText("Minutes (0-59)")

        self._sec_input = QLineEdit(self)
        self._sec_input.setPlaceholderText("Seconds (0-59)")

        hours_validate = QIntValidator(0, 11, self)
        self._hours_input.setValidator(hours_validate)

        min_validate = QIntValidator(0, 59, self)
        self._min_input.setValidator(min_validate)

        secs_validate = QIntValidator(0, 59, self)
        self._sec_input.setValidator(secs_validate)

        self._confirm_button = QPushButton("Confirm", self)

        layout = QHBoxLayout(self)
        layout.addWidget(self._hours_input)
        layout.addWidget(self._min_input)
        layout.addWidget(self._sec_input)

        final_layout = QVBoxLayout(self)
        final_layout.addLayout(layout)
        final_layout.addWidget(self._confirm_button)

        self._confirm_button.clicked.connect(self._confirm_input)

    def _confirm_input(self):
        if self._hours_input.text() and self._min_input.text() and self._sec_input.text():
            hours = int(self._hours_input.text())
            minutes = int(self._min_input.text())
            seconds = int(self._sec_input.text())

        self.time_entered.emit(hours, minutes, seconds)