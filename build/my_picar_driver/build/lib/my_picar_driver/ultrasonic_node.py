import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from picarx import Picarx

class UltraSonicNode(Node):
    def __init__(self):
        super().__init__('ultrasonic_node')
        self.us_publisher = self.create_publisher(Range,'/ultrasonic/range',10)
        self.us_timer = self.create_timer(0.05, self.timer_callback)

        self.picarx = Picarx()
        self.get_logger().info('Ultrasonic node has been Started!')

    def timer_callback(self):
        distance = self.picarx.get_distance()
        if distance >= 0:
            ultrasonic_msg = Range()
            ultrasonic_msg.header.stamp = self.get_clock().now().to_msg()
            ultrasonic_msg.header.frame_id = 'ultrasonic_link'
            ultrasonic_msg.radiation_type = Range.ULTRASOUND
            ultrasonic_msg.field_of_view = 0.5  # Example FOV in radians
            ultrasonic_msg.min_range = 0.02  # Minimum range in meters
            ultrasonic_msg.max_range = 4.0   # Maximum range in meters
            ultrasonic_msg.range = float(distance/100.0)
            self.us_publisher.publish(ultrasonic_msg)
        else:
            self.get_logger().warn('Failed to read distance from ultrasonic sensor')

def main(args = None):
    rclpy.init(args=args)
    ultrasonic_node = UltraSonicNode()
    rclpy.spin(ultrasonic_node)
    ultrasonic_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

