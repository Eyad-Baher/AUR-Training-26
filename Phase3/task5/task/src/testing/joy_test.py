import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy

class TestFirmwareNode(Node):
    def __init__(self):
        super().__init__('test_firmware_node')
        
        self.subscription = self.create_subscription(
            Joy,
            '/joy',
            self.listener_callback,
            10
        )
        self.get_logger().info(' Listening for Keyboard commands...')

    def listener_callback(self, msg):
        throttle = msg.axes[0]
        steering = msg.axes[1]
        gripper = msg.buttons[0]
        
        self.get_logger().info(
            f'Received -> Throttle (W/S): {throttle} | Steering (A/D): {steering} | Gripper (G): {gripper}'
        )

def main(args=None):
    rclpy.init(args=args)
    node = TestFirmwareNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()