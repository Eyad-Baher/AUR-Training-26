import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class TestPublisher(Node):
    def __init__(self):
        super().__init__('test_publisher_node')
        
        self.publisher_ = self.create_publisher(Float32, '/robot/battery', 10)
        
        self.battery_timer = self.create_timer(1.0, self.publish_battery)
        
        self.battery = 1.0

    def publish_battery(self):
        msg = Float32()
        msg.data = self.battery
        self.publisher_.publish(msg)
        
        self.get_logger().info(f'Publishing Battery Level: {self.battery:.1f}')

        self.battery -= 0.1

        if self.battery < 0.0:
            self.battery = 1.0

def main(args=None):
    rclpy.init(args=args)
    node = TestPublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()