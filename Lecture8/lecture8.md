# ROS2_Study Lecture8

# Topic 프로그래밍 - Python

# Publisher Node 작성

### 코드분석

다음 페이지에 있는 코드를 분석해본다.

[gcamp_ros2_basic/cmd_vel_pub.py at main · Road-Balance/gcamp_ros2_basic](https://github.com/Road-Balance/gcamp_ros2_basic/blob/main/py_topic_pkg/py_topic_pkg/cmd_vel_pub.py)

- shebang line - windows에서는 의미 X
- 이 프로그램이 어떠한 언어로 쓰였다는 것을 명시

```python
#!/usr/bin/env python3
```

- geometry_msgs/msg/Twist  ⇒ `from geometry_msgs.msg import Twist`
- rclpy, message type인 Twist를 import

```bash
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
```

- `rclpy.spin` 은 기본적으로 계속해서 주기적으로 Node를 동작
→ 따라서 로봇 무한 회전

```python
def main(args=None):
		#rclpy 초기화
    rclpy.init(args=args)
		
		# 새로운 Node에 해당하는 무언가 생성
    cmd_vel_publisher = CmdVelPublisher()

		# rclpy에게 이 Node를 반복해서 실행 (=spin) 하라고 전달
		# spin 안에 while문이 포함
    rclpy.spin(cmd_vel_publisher)

		# Node의 실행 중 여러 상태들에 대한 로그, 잘 실행되는지 확인. 
    cmd_vel_publisher.get_logger().info('\n==== Stop Publishing ====')

		# 사용을 마친 생성물 종료
    cmd_vel_publisher.destroy_node()

		# 마찬가지로 사용을 마친 Node는 종료
    rclpy.shutdown()
```

- 만약 일정시간동안만 움직이고 싶을 땐 아래처럼 while문을 이용

```python
def main(args=None):
		
    rclpy.init(args=args)

    cmd_vel_publisher = CmdVelPublisher()
		
		# 기본적으로 CPU clock을 사용하기 때문에 절대 시간과 정확히 일치한다는 보장은 없음
		# 시간을 초단위로 볼 수 있는 함수
    start_time = cmd_vel_publisher.get_clock().now().to_msg().sec
    clock_now  = start_time
		time_delta = 0

		# 5초 동안만 실행하기 위한 While문 사용
    while (clock_now - start_time) < 5:
				# spin_once -> 한번만 spin
				# spin은 무한루프이므로 탈출해야함
        rclpy.**spin_once**(cmd_vel_publisher)
        clock_now = cmd_vel_publisher.get_clock().now().to_msg().sec

        time_delta = clock_now - start_time
				#시간 출력
        print(f'{time_delta} seconds passed')

		# 나머지는 이전 예제와 동일
    cmd_vel_publisher.stop_robot()

    cmd_vel_publisher.get_logger().info('\n==== Stop Publishing ====')
    cmd_vel_publisher.destroy_node()

    rclpy.shutdown()
```

- ROS2의 거의 모든 개발은 Class 형태로 개발, Class형태의  더불어 모든 Class는 Node를 기본적으로 상속받음. 이 Node안에 수적인 기능들이 모두 구현 (Composition)
- 상속이란, 상위 Class가 구현해 둔 것을 추가 개발 없이 동일하게 사용할 수 있다는 것과 더불어, 상속받은 Class 자신만의 기능을 추가할 수 있다는 뜻

```python
class CmdVelPublisher(Node):

    def __init__(self):
        super().__init__("cmd_vel_pub_node")
				# publisher를 생성
        self.publisher = self.create_publisher(Twist, "skidbot/cmd_vel", 10)

				# 어느정도의 주기로 publish 할 것인지를 선택
				# 5초의 간격으로 publish_callback 함수를 반복 실행
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, **self.publish_callback**)

				# 시작한다는 log를출력
        self.get_logger().info(" DriveForward node Started, move forward during 5 seconds \n")
    
    def publish_callback(self):
				...

    def stop_robot(self):
        ...
```

### create_publisher

- `Twist` : Topic 통신에 사용될 Message Type
- `"skidbot/cmd_vel"` : 이 Topic의 이름을 지정
- `10` : 대기열의 크기 (쓰레기가 어느정도 쌓이면 모아서 버림)(적절한 데이터를 쌓아둠)

 `publish_callback` 함수

```python
		def publish_callback(self):
				# 상단 형식에 맞추어 Twist Message를 채워줍니다.

				# 전방 속도 0.5 / 각속도 1.0 => 원 운동
        twist_msg = Twist()
        twist_msg.linear.x  = 0.5
        twist_msg.angular.z = 1.0
        **self.publisher.publish(twist_msg)**

    def stop_robot(self):
        stop_msg = Twist()

				# 전방 속도 0.0 / 각속도 0.0 => 정지
        stop_msg.linear.x  = 0.0
        stop_msg.angular.z = 0.0
        self.publisher.publish(stop_msg)
```

다음 함수를 통해 publisher에게 callback을 해줄 수 있다.

또한 twist_msg를 수정하여 로봇의 움직임을 수정해보았다.

```python
def publish_callback(self):
twist_msg = Twist()
twist_msg.linear.x = 1.0
twist_msg.angular.z = 0.0
self.publisher.publish(twist_msg)
```

![Untitled](ROS2_Study%20Lecture8%207e150ab1a6c24010943e6e1ae5769a05/Untitled.png)

코드를 수정하고 실행 한 결과 로봇이 직진을 하는것을 확인할 수 있었다.