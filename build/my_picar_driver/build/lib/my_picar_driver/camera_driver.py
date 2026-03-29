import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraDriver(Node):
    def __init__(self):
        super().__init__('camera_node')
        self.cam_publisher = self.create_publisher(Image,'/camera/image_raw',10)
        self.cam_timer = self.create_timer(0.05, self.timer_callback)

        #initialising CV2 and CvBridge
        self.bridge = CvBridge()
        self.cap = cv2.VideoCapture(0)

        self.get_logger().info('Camera node has been Started!')

    def timer_callback(self):
        for _ in range(5):
            self.cap.grab()
    
        ret, frame = self.cap.retrieve() # Now get the actual image
         # Capture frame-by-frame and ret is a boolean variable
        if ret:
            #we convert the opencv image to ROS image message
            ros_image = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
            ros_image.header.frame_id = 'camera_link'
            self.cam_publisher.publish(ros_image)
        else:
            self.get_logger().warn('Failed to capture image from camera')

    def __del__(self):
        self.cap.release()
        self.get_logger().info('Camera node has been Stopped!')

def main(args = None):
    rclpy.init(args=args)
    camera_node = CameraDriver()
    rclpy.spin(camera_node)
    camera_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
