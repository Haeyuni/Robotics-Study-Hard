import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class Battery_pub(Node):
    def __init__(self):
        super().__init__('battery_pub')
        self.pub = self.create_publisher(Int32, 'battery', 10)
        self.create_timer(2.0, self.tick)
        self.level = 100

    def tick(self):
        msg = Int32()
        msg.data = self.level
        self.pub.publish(msg)
        self.get_logger().info('battery: '+ str(self.level))
        self.level -= 1

def main():
    rclpy.init()
    rclpy.spin(Battery_pub())
    rclpy.shutdown()