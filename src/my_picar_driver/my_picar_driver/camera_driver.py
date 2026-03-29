import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraDriver(Node):
    def __init__(self):
        super().__init__('camera_node')
        # Using a slightly larger queue size for the publisher
        self.cam_publisher = self.create_publisher(Image, '/camera/image_raw', 10)
        
        # SLOWED DOWN: 10 FPS (0.1) is much more stable for Pi -> VM streaming
        self.cam_timer = self.create_timer(1.0, self.timer_callback)

        self.bridge = CvBridge()
        self.cap = cv2.VideoCapture(0)

        # Set hardware resolution at the source (OpenCV level)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.get_logger().info('Camera node has been Started with Bandwidth Optimization!')

    def timer_callback(self):
        # Read the frame
        ret, frame = self.cap.read()
        
        if ret:
            # REDUCE DATA SIZE: Resizing to 320x240 reduces bandwidth by 75%
            # This is the "Magic Fix" for the buffer overflow error
            small_frame = cv2.resize(frame, (320, 240))

            # Convert to ROS image message
            ros_image = self.bridge.cv2_to_imgmsg(small_frame, encoding='bgr8')
            
            # ADD METADATA: RViz needs these to show the image in the 3D view
            ros_image.header.stamp = self.get_clock().now().to_msg()
            ros_image.header.frame_id = 'camera_link'
            
            self.cam_publisher.publish(ros_image)
        else:
            self.get_logger().warn('Failed to capture image from camera')

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
        self.get_logger().info('Camera node has been Stopped!')

def main(args=None):
    rclpy.init(args=args)
    camera_node = CameraDriver()
    try:
        rclpy.spin(camera_node)
    except KeyboardInterrupt:
        pass
    finally:
        camera_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()