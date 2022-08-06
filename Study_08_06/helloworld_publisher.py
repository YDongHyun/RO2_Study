import rclpy
from rclpy.node import Node
# publisher의 Qos설정을 위해 import
from rclpy.qos import QoSProfile
# string 메세지 인터페이스 사용을 위해 import
from std_msgs.msg import String

class HelloworldPublisher(Node):
    def __init__(self):
        # 클래스 생성자 정의, Node의 생성자를 호출, 노드이름을 helloworld_publisher로 설정
        super().__init__('helloworld_publisher')
        # QoSProfile을 호출하여  Qos설정. (publish할 데이터를 버퍼에 10개까지 저장)
        qos_profile = QoSProfile(depth=10)
        # publisher 생성, msg type = String, Qos=qos_profile  publisher name = subscriber name
        self.helloworld_publisher=self.create_publisher(String,'helloworld',qos_profile)
        # create_timer 함수로 callback함수 1초마다 publish_helloworld.msg 실행
        self.timer = self.create_timer(1,self.publish_helloworld_msg)
        self.count=0

    # callback 함수
    def publish_helloworld_msg(self):
        # Sting으로 설정하였으나 실질적으로 msg.data 변수에 저장
        msg=String()
        # 카운드 값이 증가하면서 숫자가 바뀜
        msg.data='Hello World:{0}'.format(self.count)
        # publish
        self.helloworld_publisher.publish(msg)
        # get_logger함수를 통해 터미널에 출력
        self.get_logger().info('Publish message:{0}'.format(msg.data))
        self.count+=1

def main(args=None):
    # 초기화
    rclpy.init(args=args)
    # node 변수로 생성import rclpy
from rclpy.node import Node
# publisher의 Qos설정을 위해 import
from rclpy.qos import QoSProfile
# string 메세지 인터페이스 사용을 위해 import
from std_msgs.msg import String

class HelloworldPublisher(Node):
    def __init__(self):
        # 클래스 생성자 정의, Node의 생성자를 호출, 노드이름을 helloworld_publisher로 설정
        super().__init__('helloworld_publisher')
        # QoSProfile을 호출하여  Qos설정. (publish할 데이터를 버퍼에 10개까지 저장)
        qos_profile = QoSProfile(depth=10)
        # publisher 생성, msg type = String, Qos=qos_profile  publisher name = subscriber name
        self.helloworld_publisher=self.create_publisher(String,'helloworld',qos_profile)
        # create_timer 함수로 callback함수 1초마다 publish_helloworld.msg 실행
        self.timer = self.create_timer(1,self.publish_helloworld_msg)
        self.count=0

    # callback 함수
    def publish_helloworld_msg(self):
        # Sting으로 설정하였으나 실질적으로 msg.data 변수에 저장
        msg=String()
        # 카운드 값이 증가하면서 숫자가 바뀜
        msg.data='Hello World:{0}'.format(self.count)
        # publish
        self.helloworld_publisher.publish(msg)
        # get_logger함수를 통해 터미널에 출력
        self.get_logger().info('Publish message:{0}'.format(msg.data))
        self.count+=1

def main(args=None):
    # 초기화
    rclpy.init(args=args)
    # node 변수로 생성
    node=HelloworldPublisher()
    try:
        # spin으로 node 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # ctrl+c 종료
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        # node 종료
        node.destroy_node()
        rclpy.shutdown()import rclpy
from rclpy.node import Node
# publisher의 Qos설정을 위해 import
from rclpy.qos import QoSProfile
# string 메세지 인터페이스 사용을 위해 import
from std_msgs.msg import String

class HelloworldPublisher(Node):
    def __init__(self):
        # 클래스 생성자 정의, Node의 생성자를 호출, 노드이름을 helloworld_publisher로 설정
        super().__init__('helloworld_publisher')
        # QoSProfile을 호출하여  Qos설정. (publish할 데이터를 버퍼에 10개까지 저장)
        qos_profile = QoSProfile(depth=10)
        # publisher 생성, msg type = String, Qos=qos_profile  publisher name = subscriber name
        self.helloworld_publisher=self.create_publisher(String,'helloworld',qos_profile)
        # create_timer 함수로 callback함수 1초마다 publish_helloworld.msg 실행
        self.timer = self.create_timer(1,self.publish_helloworld_msg)
        self.count=0

    # callback 함수
    def publish_helloworld_msg(self):
        # Sting으로 설정하였으나 실질적으로 msg.data 변수에 저장
        msg=String()
        # 카운드 값이 증가하면서 숫자가 바뀜
        msg.data='Hello World:{0}'.format(self.count)
        # publish
        self.helloworld_publisher.publish(msg)
        # get_logger함수를 통해 터미널에 출력
        self.get_logger().info('Publish message:{0}'.format(msg.data))
        self.count+=1

def main(args=None):
    # 초기화
    rclpy.init(args=args)
    # node 변수로 생성
    node=HelloworldPublisher()
    try:
        # spin으로 node 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # ctrl+c 종료
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        # node 종료
        node.destroy_node()
        rclpy.shutdown()

if __name__=='__main__':
    main()

if __name__=='__main__':
    main()
    node=HelloworldPublisher()
    try:
        # spin으로 node 실행
        rclpy.spin(node)
    except KeyboardInterrupt:
        # ctrl+c 종료
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        # node 종료
        node.destroy_node()
        rclpy.shutdown()

if __name__=='__main__':
    main()
