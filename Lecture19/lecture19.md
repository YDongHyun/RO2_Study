# 중간 프로젝트 - Maze World2

저번 18번 강의에서는 Maze World 예제를 실행하였다.

이번 강의에서는 코드를 분석하였다.

## Maze Action Server 작성

지속적으로 로봇의 동향을 알려주기 위해 Action을 사용하였다.

먼저 아래 코드 Action타입을 살펴보았다.

```bash
$ ros2 interface show custom_interfaces/action/Maze
```

![Untitled](https://user-images.githubusercontent.com/80799025/181170587-48160849-352a-4fce-be56-77d100e131d6.png)

다음과 같은 Action의 타입을 확인할 수 있었다.

다음은 server의 코드를 분석해보았다.

### 특정 방향 로봇 회전

```python
# odom을 사용, quaterninon을 사용하기 때문에 euler로 변환
from py_action_pkg.robot_controller import euler_from_quaternion
from nav_msgs.msg import Odometry
...

				self.odom_sub = self.create_subscription(
            Odometry, "/diffbot/odom", self.odom_sub_cb, 10
        )

...

def turn_robot(self, euler_angle):
    self.get_logger().info(f'Robot Turns to {euler_angle}')

    turn_offset = 100
		
		# 각도 한계를 너무 적게 주면, 0 -> -3.14로 갑자기 변해버리는 오류 발생
    while abs(turn_offset) > 0.087:
				# P Gain Control, 급작스러운 변화를 막아준다
        turn_offset = 0.7 * (euler_angle - self.yaw)
        self.twist_msg.linear.x = 0.0
        self.twist_msg.angular.z = turn_offset
        self.cmd_vel_pub.publish(self.twist_msg)
			
		# 로봇 정지
    self.stop_robot()
```

### 충돌 전까지 로봇 전진

```python
	# 일전에 과제로 했던 parking예제와 비슷
	# LaserScan import
	from sensor_msgs.msg import LaserScan
		...

				self.laser_sub = self.**create_subscription**(
            LaserScan, "/diffbot/scan", self.laser_sub_cb, 10
        )

		...
	# range[360]은 전방을 의미한다.
	def laser_sub_cb(self, data):
        self.forward_distance = data.ranges[360]
		...

	def parking_robot(self):
		# 거리가 1 이하면 로봇 정지
    while self.forward_distance > 1.0:
        self.twist_msg.linear.x = 0.5
        self.twist_msg.angular.z = 0.0

        self.cmd_vel_pub.publish(self.twist_msg)
	
	#로봇 정지
    self.stop_robot()
```

### 초록 박스 인식

```python
from py_action_pkg.image_sub import ImageSubscriber

...
				for _, val in enumerate(goal_handle.request.turning_sequence):
            self.get_logger().info(f'Current Cmd: {val}')

            feedback.feedback_msg = f"Turning {direction_str_dict[val]}"

            self.turn_robot(direction_dict[val])
            self.parking_robot()

            goal_handle.publish_feedback(feedback)

				# 모든 execution을 마친 시점에서,ImageSubscriber실행 (전방의 중간의 이미지를 얻음)
        image_sub_node = ImageSubscriber()
        rclpy.spin_once(image_sub_node)
        center_pixel = image_sub_node.center_pixel

				# 전방 pixel값을 인식, 초록박스 앞인지 판단
        if sum(center_pixel) < 300 and center_pixel[1] > 100:
            goal_handle.succeed()
						# 초록 박스 앞이면 succeed 로그 출력
            self.get_logger().warn("==== Succeed ====")
            result = Maze.Result()
            result.success = True
        else:
            goal_handle.abort()
						# 이외는 fail 로그 출력
            self.get_logger().error("==== Fail ====")
            result = Maze.Result()
            result.success = False

        return result
```

## Maze Action Client 작성

Server를 살펴보았으니 Client를 살펴보았다.

Client가 하는일을 복습하면

- 사용자로 부터 Goal을 받은 후 Send
- 지속적으로 feedback_msg 출력

### main

```python
def main(args=None):
    rclpy.init(args=args)

    maze_action_client = MazeActionClient()
		# 사용자의 입력을 받아둘 리스트 생성
    user_inputs = []
    # Input Logic
    try:
        maze_action_client.get_logger().info('Enter numbers [or stop] : ')
		# 사용자로부터 input을 받음
        while True:
            user_inputs.append(int(input()))
    # if the input is not-integer, just print the list
    except:
		# sequencelist 출력
        maze_action_client.get_logger().info(f'Your sequence list : {user_inputs}')
    maze_action_client.get_logger().info('==== Sending Goal ====')
    future = maze_action_client.send_goal(user_inputs)

    rclpy.spin(maze_action_client)
```

## Namespace & Prefix

namespace란, 예로들어 로봇 `diffbot`이 있다고 가정하였다.

- `/diffbot/scan`
- `/diffbot/odom`
- `/diffbot/cmd_vel`

위와 같이 diffbot이라는 이름을 그대로 사용하였다.

만약 위 같은 상황에서 다른 로봇을 소환한다면, diffbot 부분 코드를 일일이 다 바꿔야 할것이다

이를 해결하기 위해 namespace를 이용한다.

```bash
		maze_action_srv_node = Node(
        package='py_action_pkg',
				#namespace에 로봇 이름 지정
        namespace='diffbot',
        executable='maze_action_server',
        name='maze_action_server',
        output='screen'
    )
```

launch file에서 이 옵션에 지정된 값으로 Node안에 통신이 이루어진다.

만약 namespace를 바꾸면 diffbot이 아닌 다른 이름으로 통신이 이루어진다.

Prefix란 접두사로, 노드의 통신명 이름 앞에 붙는것을 Prefix라 한다.

**namespace를 사용하기 위해 다음과 같은 과정이 필요하다.**

- 기존의 이름이 붙언 토픽 이름을 모두 변경
- launch file을 작성하여 이때 namespace  option을 지정한다.

```python
def generate_launch_description():

    maze_action_srv_node = Node(
        package='py_action_pkg',
        namespace='diffbot', # <- 다음과 같이 지정
        executable='maze_action_server',
        name='maze_action_server',
        output='screen'
    )
```

- setup.py에 launch file을 추가한다.

```python
# glob 모듈을 import
from glob import glob
import os
from setuptools import setup

package_name = 'py_action_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
				# launch file 추가
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ]
```
