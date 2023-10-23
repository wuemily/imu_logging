import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, MagneticField, Temperature

from std_msgs.msg import String

class ImuLogger(Node):

    def __init__(self):
        super().__init__('imu_logger')
        self.old_x = 0.0 #initally orientation is 0
        self.old_y = 0.0
        self.old_z = 0.0
        self.prev_time = self.get_clock().now().seconds_nanoseconds()
        self.prev_accel_x = -9.8
        self.prev_accel_y = 0.0
        self.prev_accel_z = 0.0
        self.start_time = 0.0
        self.first_msg_received = False
        self.prev_not_upright = False
        self.subscription = self.create_subscription(Imu, 'bno055/imu_raw', self.logger_callback, 10)
        self.subscription

    def logger_callback(self, msg):
        if not self.first_msg_received :
            self.start_time = self.get_clock().now()
            self.first_msg_received = True
        
        # Print orientation
        # self.get_logger().info(f'Orientation (x, y, z): ({msg.orientation.x}, {msg.orientation.y}, {msg.orientation.z})', throttle_duration_sec=10)
        # self.get_logger().info('Angular Velocity x: "%d"' % msg.angular_velocity.x, throttle_duration_sec=10)

        # Print linear velocity every 5 seconds
        delta_t = (self.get_clock().now().seconds_nanoseconds()[0] - self.prev_time[0]) + 0.000000001 * (self.get_clock().now().seconds_nanoseconds()[1] - self.prev_time[1])
        vel_x = (msg.orientation.x - self.old_x) / delta_t
        vel_y = (msg.orientation.y - self.old_y) / delta_t
        vel_z = (msg.orientation.z - self.old_z) / delta_t

        self.old_x = msg.orientation.x #update old values
        self.old_y = msg.orientation.y
        self.old_z = msg.orientation.z
        self.prev_time = self.get_clock().now().seconds_nanoseconds()

        # what is the unit of velocity?? 
        self.get_logger().info(f'Linear Velocity (x, y, z): ({vel_x}, {vel_y}, {vel_z})', skip_first=True, throttle_duration_sec=5)

        # Sudden acceleration
        if (abs(msg.linear_acceleration.x - self.prev_accel_x) > 5.0) :
            self.get_logger().error('Sudden acceleration in x')
        if (abs(msg.linear_acceleration.y - self.prev_accel_y) > 5.0) :
            self.get_logger().error('Sudden acceleration in y')
        if (abs(msg.linear_acceleration.z - self.prev_accel_z) > 5.0) :
            self.get_logger().error('Sudden acceleration in z')

        # Update prev accel
        self.prev_accel_x = msg.linear_acceleration.x
        self.prev_accel_y = msg.linear_acceleration.y
        self.prev_accel_z = msg.linear_acceleration.z

        if (msg.linear_acceleration.z >= 8.0 and self.prev_not_upright) :
            self.prev_not_upright = False
            self.get_logger().error('IMU returned to upright position')

        # IMU upside down; maybe use quaternion??
        if (msg.linear_acceleration.z < 8.0 and msg.linear_acceleration.z > 0.0) :
            self.prev_not_upright = True
            self.get_logger().error('IMU is not upright', throttle_duration_sec=3)
        elif (msg.linear_acceleration.z < 0.0) :
            self.prev_not_upright = True
            self.get_logger().error('IMU is upside down', throttle_duration_sec=3)


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