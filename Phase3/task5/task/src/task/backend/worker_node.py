from rclpy.node import Node
from std_msgs.msg import Float32


class WorkerNode(Node):

    def __init__(self, on_battery):
        super().__init__('worker_node')
        self._on_battery = on_battery
        self.create_subscription(Float32, '/robot/battery', self._battery_callback, 10)

    def _battery_callback(self, msg):
        level = max(0.0, min(1.0, float(msg.data)))  
        self._on_battery(level)