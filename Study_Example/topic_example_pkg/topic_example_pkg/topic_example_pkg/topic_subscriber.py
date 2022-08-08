import queue
import rclpy
from rclpy.node import Node
from msg_example.msg import Num

class topic_example_sub(Node):
    def __init__(self):
        super().__init__('topic_example_sub')
        self.subscriber=self.create_subscription(
            Num, 'topic_ex', self.sub_callback, queue_size=10
        ) 
        self. subscriber

    def sub_callback(self,msg):
        topic_msg=Num()
        topic_msg.x='time : {0} '.format(self.count)
        self.get_logger().info("topic_sub : {0}").format(topic_msg.x)    
    
def main(args=None):
    rclpy.init(args=args)
    node=topic_example_sub()
    rclpy.spin(node)

if __name__=='__main__':
    main()