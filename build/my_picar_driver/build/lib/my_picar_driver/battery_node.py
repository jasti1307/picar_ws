import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from robot_hat import ADC


class BatteryNode(Node):
    def __init__(self):
        super().__init__('battery_node')

        self.battery_publisher = self.create_publisher(Float32, 'battery_state', 10)

        self.adc = ADC("A4")

        self.battery_timer = self.create_timer(5, self.timer_callback)
        self.get_logger().info('Battery_node has been Started!')

    def timer_callback(self):
        # 1. Read ADC and convert to Voltage
        value = self.adc.read()
        voltage = (value * 3.3) / 4095 * 3
        
        # 2. Calculate Percentage
        # 8.4V = 100%, 6.0V = 0%
        percentage = ((voltage - 6.0) / (8.4 - 6.0)) * 100
        
        # 3. Clamp the value between 0 and 100
        final_percentage = max(0.0, min(100.0, percentage))

        # 4. Publish as a simple Float
        msg = Float32()
        msg.data = float(final_percentage)
        self.battery_publisher.publish(msg)

        # Log it so you can see it in the terminal
        self.get_logger().info(f'Battery: {final_percentage:.1f}% ({voltage:.2f}V)')

def main(args=None):
    rclpy.init(args=args)
    battery_node = BatteryNode()
    rclpy.spin(battery_node)
    battery_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()








