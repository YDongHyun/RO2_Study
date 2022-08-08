from msg_example.msg import Num
import rclpy
from rclpy.node import Node

class topic_example_pub(Node):
    def __init__(self):
        super().__init__('topic_example')
        self.publisher=self.create_publisher(Num,"topic_ex",10)
        self.timer = self.create_timer(1,self.publish_callback)
        self.get_logger().info("test")
        self.count=0
    
    def publish_callback(self):
        topic_msg=Num()
        topic_msg.x='time : {0} '.format(self.count)
        self.publisher.publish(topic_msg)
        self.get_logger().info('pubmsg : {0}').format(topic_msg.x)
        self.count+=1

def main(args=None):
    rclpy.init(args=args)
    node=topic_example_pub()
    rclpy.spin(node)

if __name__=='__main__':
    main()
