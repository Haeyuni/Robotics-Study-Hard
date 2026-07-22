import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        # node name: talker
        super().__init__('talker')
        self.pub = self.create_publisher(String, 'chatter', 10)
        self.create_timer(1.0, self.tick)

    def tick(self):
        msg = String()
        msg.data = 'hello'
        self.pub.publish(msg)
        self.get_logger().info('send: '+msg.data)

def main():
    rclpy.init()
    rclpy.spin(Talker())
    rclpy.shutdown()