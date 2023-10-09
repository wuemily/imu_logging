import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, MagneticField, Temperature

from std_msgs.msg import String

class ImuLogger(Node):

    def __init__(self):
        super().__init__('imu_logger')
        self.prev_accel_x = 0.0
        self.prev_accel_y = 0.0
        self.prev_accel_z = 0.0
        self.start_time = 0.0
        self.first_msg_received = False
        self.subscription = self.create_subscription(Imu, 'bno055/imu_raw', self.logger_callback, 10)
        self.subscription

    def logger_callback(self, msg):
        if not first_msg_received :
            start_time = self.get_clock().now()
            first_msg_received = True
        
        # Print orientation
        # self.get_logger().info(f'Orientation (x, y, z): ({msg.orientation.x}, {msg.orientation.y}, {msg.orientation.z})', throttle_duration_sec=10)
        # self.get_logger().info('Angular Velocity x: "%d"' % msg.angular_velocity.x, throttle_duration_sec=10)

        # Print linear velocity
        self.get_logger().info(f'Linear Velocity (x, y, z): ({msg.orientation.x}, {msg.orientation.y}, {msg.orientation.z})', throttle_duration_sec=2)

        # Sudden acceleration
        if (msg.linear_acceleration.x > 5.0) :
            self.get_logger().error('Sudden acceleration in x')
        if (msg.linear_acceleration.y > 5.0) :
            self.get_logger().error('Sudden acceleration in y')
        if (msg.linear_acceleration.z > 5.0) :
            self.get_logger().error('Sudden acceleration in z')

        # IMU upside down; maybe use quaternion??
        if (msg.linear_acceleration.z < 8 & msg.linear_acceleration.z > 0) : 
            self.get_logger().error('IMU is not upright')
        elif (msg.linear_acceleration.z < 0) :
            self.get_logger().error('IMU is upside down')

def main(args=None):
    rclpy.init(args=args)

    logger = ImuLogger()

    rclpy.spin(logger)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    logger.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()