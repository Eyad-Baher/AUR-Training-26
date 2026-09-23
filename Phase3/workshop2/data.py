from PySide6.QtCore import QObject, Property, QTimer, Signal


class MyData(QObject):

    hours_changed = Signal()
    mins_changed = Signal()
    secs_changed = Signal()

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)

        self._hours = 0
        self._mins = 0
        self._secs = 0

        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._increment)
        self._timer.start()

    @Property(int, notify=hours_changed)
    def hours(self):
        return self._hours

    @hours.setter
    def hours(self, new: int):
        if new != self._hours and 0 <= new <= 11:
            self._hours = new
            self.hours_changed.emit()

    @Property(int, notify=mins_changed)
    def mins(self):
        return self._mins

    @mins.setter
    def mins(self, new: int):
        if new != self._mins and 0 <= new <= 59:
            self._mins = new
            self.mins_changed.emit()

    @Property(int, notify=secs_changed)
    def secs(self):
        return self._secs

    @secs.setter
    def secs(self, new: int):
        if new != self._secs and 0 <= new <= 59:
            self._secs = new
            self.secs_changed.emit()

    def _increment(self):
        self.secs += 1
        if self.secs >= 60:
            self.secs = 0
            self.mins += 1  
            if self.mins >= 60:
                self.mins = 0
                self.hours = (self._hours + 1) % 12 
        

