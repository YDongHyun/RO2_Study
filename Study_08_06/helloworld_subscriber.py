import rclpy
from rclpy.node import Node
# publisher의 Qos설정을 위해 import
from rclpy.qos import QoSProfile
# string 메세지 인터페이스 사용을 위해 import
from std_msgs.msg import String

class HelloworldSubscriber(Node):
    # Node 생성자 호출
    def __init__(self):
        super().__init__('Helloworld_subscriber')
        # Qos 설정
        qos_profile=QoSProfile(depth=10)
        # subscriber 생성  callback함수는 subscribe_topic_message
        self.helloworld_subscriber=self.create_subscription(
            String, 
            'helloworld', 
            self.subscribe_topic_message, 
            qos_profile)
    # callback 함수
    def subscribe_topic_message(self,msg):
        self.get_logger().info('Received message: {0}'.format(msg.data))

def main(args=None):
    rclpy.init(args=args)
    node=HelloworldSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger.info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__=='__main__':
    main()
