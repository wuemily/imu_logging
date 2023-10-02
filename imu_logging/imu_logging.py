import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, MagneticField, Temperature

from std_msgs.msg import String

class ImuLogger(Node):

    def __init__(self):
        super().__init__('imu_logger')
        self.subscription = self.create_subscription(String, 'bno055/imu_raw', self.logger_callback, 10)
        self.subscription

    def logger_callback(self, msg):
        self.get_logger().info('Angular Velocity x: "%d"' % msg.data.angular_velocity.x)
        if (msg.data.angular_acceleration.x > 5.0) :
            self.get_logger().info('Sudden acceleration in x')
        if (msg.data.angular_acceleration.y > 5.0) :
            self.get_logger().info('Sudden acceleration in y')
        if (msg.data.angular_acceleration.z > 5.0) :
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