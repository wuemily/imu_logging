import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, MagneticField, Temperature

from std_msgs.msg import String

class ImuLogger(Node):

    def __init__(self):
        super().__init__('imu_logger')
        self.subscription = self.create_subscription(Imu, 'bno055/imu_raw', self.logger_callback, 10)
        self.subscription

    def logger_callback(self, msg):
        # num = 4
        self.get_logger().error(f'Orientation (x, y, z): ({msg.orientation.x}, {msg.orientation.y}, {msg.orientation.z})', throttle_duration_sec=10)
        
        self.get_logger().error('Angular Velocity x: "%d"' % msg.angular_velocity.x, throttle_duration_sec=10)

        # self.get_logger().info('Angular Velocity x: "%d"' % msg.angular_velocity.x)
        if (msg.angular_velocity.x > 5.0) :
            self.get_logger().info('Sudden acceleration in x')
        if (msg.angular_velocity.y > 5.0) :
            self.get_logger().info('Sudden acceleration in y')
        if (msg.angular_velocity.z > 5.0) :
            self.get_logger().info('Sudden acceleration in z')
            

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