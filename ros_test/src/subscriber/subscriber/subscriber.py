import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class Start(Node):
    def __init__(self):
        super().__init__("subscriber")
        self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.subscriber = self.create_subscription(Pose, "/turtle1/pose", self.subscriber_callback, 10)
        self.counter = 0
        self.create_timer(0.1, self.error_calc)  
        self.target_x = 10.0
        self.target_y = 10.0
        self.current_theta = 0.0
        self.current_x = 0.0
        self.current_y = 0.0
        self.distance_error = 0.0
        self.head_error = 0.0
        self.reached = False

    def normalize_angle(self, angle):
        return math.atan2(math.sin(angle), math.cos(angle))

    def timer_callback(self):
        v = Twist()
        if abs(self.head_error) > 0.3:
            v.linear.x = 0.0
        else:
            v.linear.x = min(1.5 * self.distance_error, 2.0)

        v.angular.z = max(min(4.0 * self.head_error, 2.0), -2.0)
        self.publisher.publish(v)
        self.counter += 1

    def subscriber_callback(self, msg):
        self.current_x = msg.x
        self.current_y = msg.y
        self.current_theta = msg.theta

    def error_calc(self):
        if self.reached:
            return

        dx = self.target_x - self.current_x
        dy = self.target_y - self.current_y
        self.distance_error = math.sqrt(dx**2 + dy**2)

        desired_theta = math.atan2(dy, dx)
        self.head_error = self.normalize_angle(desired_theta - self.current_theta)

        if self.distance_error < 0.1:
            self.get_logger().info("Target reached, stopping.")
            self.publisher.publish(Twist())
            self.reached = True
        else:
            self.timer_callback()


def main():
    rclpy.init()
    node = Start()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()