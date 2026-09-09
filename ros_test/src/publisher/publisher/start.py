import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class Start(Node):
    def __init__(self):
        super().__init__("start")
        self.get_logger().info("Publisher Node Started!!")
        self.publisher = self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.counter=0
        self.create_timer(1,self.timer_callback)
 
    def timer_callback(self):
        self.get_logger().info(f"Hello {self.counter}")
        v=Twist()
        v.linear.x=1.0
        v.angular.z = 6.28
        self.publisher.publish(v)
        self.counter+=1

def main():
    rclpy.init()
    node = Start()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()