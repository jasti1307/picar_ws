import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from picarx import Picarx


class MoveRobotNode(Node):
    def __init__(self):
        super().__init__('robot_control_node')

        self.picarx = Picarx()

        self.motion_subscriber = self.create_subscription(Twist, 'cmd_vel', self.motion_callback, 10)
        self.servo_horizontal_subscriber_ = self.create_subscription(Twist, 'servo_cam_horizontal', self.servo_horizontal_callback, 10)
        self.servo_vertical_subscriber_ = self.create_subscription(Twist, 'servo_cam_vertical', self.servo_vertical_callback, 10)

        self.get_logger().info('MoveRobotNode has been started.')

    def motion_callback(self, msg):
        linear_x = msg.linear.x
        angular_z = msg.angular.z

        # --- Drive Logic ---
        if linear_x >= 0:
            self.picarx.forward(int(linear_x * 20))
        else:
            self.picarx.backward(int(abs(linear_x) * 20))

        # --- Intuitive Steering Mapping ---
        center = -25

        if angular_z > 0:
            # Sliding LEFT (Positive) -> Moves toward 10
            target_angle = center + (-angular_z * 40)
        elif angular_z < 0:
            # Sliding RIGHT (Negative) -> Moves toward -60
            # Since angular_z is negative, adding it moves the number 'down'
            target_angle = center + (-angular_z * 40)
        else:
            target_angle = center

        # Final Safety Clamp to prevent chassis hits
        if target_angle > 10: target_angle = 0
        if target_angle < -60: target_angle = -50

        # Execute
        self.picarx.dir_current_angle = int(target_angle)
        self.picarx.dir_servo_pin.angle(int(target_angle))


    def servo_horizontal_callback(self, msg):
        horizontal_angle = msg.angular.z

        self.picarx.set_cam_pan_angle(int(horizontal_angle * 45) - 10)

    def servo_vertical_callback(self, msg):
        vertical_angle = msg.angular.z

        self.picarx.set_cam_tilt_angle(int(vertical_angle * 45))

    
def main(args=None):   
    rclpy.init(args=args)
    move_robot_node = MoveRobotNode()
    rclpy.spin(move_robot_node)
    move_robot_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()