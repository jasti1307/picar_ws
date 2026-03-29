import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray
from picarx import Picarx

class GrayScaleNode(Node):
    def __init__(self):
        super().__init__('gray_scale_node')

        self.picarx = Picarx()

        self.gray_scale_publisher = self.create_publisher(Int32MultiArray, 'gray_scale', 10)
        self.timer = self.create_timer(3, self.timer_callback)
        self.get_logger().info('GrayScale Node has been Started!')

    def timer_callback(self):
        msg = Int32MultiArray()

        raw_data = self.picarx.get_grayscale_data()

        msg.data = [int(x) for x in raw_data]

        self.gray_scale_publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    gray_scale_node = GrayScaleNode()    
    rclpy.spin(gray_scale_node)
    gray_scale_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()





    


