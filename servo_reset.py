from picarx import Picarx
import time

px = Picarx()
# This forces the library to write a fresh 0 to its internal state
px.set_dir_servo_angle(0) 
time.sleep(1)
print("Servo state reset to 0. Now try your ROS node.")