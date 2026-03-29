import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
import time
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32MultiArray

class SafetyNode(Node):
    def __init__(self):
        super().__init__('safety_node')

        self.us_safety_subscriber = self.create_subscription(Range,
            '/ultrasonic/range',
            self.ultrasonic_callback,
            10)
        self.gs_safety_subscriber = self.create_subscription(Int32MultiArray,
            '/gray_scale',
            self.gray_scale_callback,
            10)
        
        self.get_logger().info('Safety node has been Started!')

        self.stop_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.safe_distance = 0.2  # Safe distance in meters
    
    def ultrasonic_callback(self, msg):
        distance = msg.range
        if distance < self.safe_distance:
            self.get_logger().info('Obstacle ahead at distance: {:.2f} m. Stopping the car.'.format(distance))
            stop_msg = Twist()
            stop_msg.linear.x = 0.0
            stop_msg.angular.z = 0.0
            self.stop_publisher.publish(stop_msg)

    def gray_scale_callback(self, msg):
        gray_values = msg.data
        threshold = 700  # Example threshold for detecting a line
        for value in gray_values:
            if value < threshold:
                self.get_logger().info('Cliff detected! Stopping the car.')
                stop_msg = Twist()
                stop_msg.linear.x = 0.0
                stop_msg.angular.z = 0.0
                self.stop_publisher.publish(stop_msg)

def main(args = None):
    rclpy.init(args=args)
    safety_node = SafetyNode()
    rclpy.spin(safety_node)
    safety_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
