import threading

import rclpy
from rclpy.executors import MultiThreadedExecutor
from PySide6.QtCore import QCoreApplication, QObject, Property, Qt, Signal, Slot

from task.backend.joy_node import JoyNode
from task.backend.worker_node import WorkerNode


class Mediator(QObject):
    """Bridge between the ROS nodes and the QML/GUI."""

    batteryLevelChanged = Signal()
    _battery_received = Signal(float) 

    def __init__(self, parent=None):
        super().__init__(parent)
        self._battery = 0.0

       
        self._battery_received.connect(
            self._set_battery, Qt.ConnectionType.QueuedConnection)

        if not rclpy.ok():
            rclpy.init()
        self._worker = WorkerNode(self._battery_received.emit)
        self._joy = JoyNode()

        self._executor = MultiThreadedExecutor()
        self._executor.add_node(self._worker)
        self._executor.add_node(self._joy)
        threading.Thread(target=self._executor.spin, daemon=True).start()

        QCoreApplication.instance().aboutToQuit.connect(self.shutdown)

    def _get_battery(self):
        return self._battery

    batteryLevel = Property(float, _get_battery, notify=batteryLevelChanged)

    @Slot(float)
    def _set_battery(self, value):
        self._battery = value
        self.batteryLevelChanged.emit()

    @Slot()
    def trigger_emergency(self):
        self._joy.trigger_emergency()

    def shutdown(self):
        self._executor.shutdown()
        self._worker.destroy_node()
        self._joy.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()