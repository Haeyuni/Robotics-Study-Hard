import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class Speed_pub(Node):
    def __init__(self):
        super().__init__('speed_pub')
        self.pub = self.create_publisher(Float32, 'speed', 10)
        self.create_timer(0.5, self.tick)
        self.level = 0.0

    def tick(self):
        msg = Float32()
        msg.data = self.level
        self.pub.publish(msg)
        self.get_logger().info('speed: '+str(self.level))
        self.level += 0.1

def main():
    rclpy.init()
    rclpy.spin(Speed_pub())
    rclpy.shutdown()