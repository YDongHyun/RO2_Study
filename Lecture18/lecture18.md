# 중간 프로젝트 Maze World

로봇이 미로를 탈출 할 수 있도록 하는 예제

## ROS2 Description

먼저 프로젝트를 시작하기 전에 로봇에 여러 형태에 대해여 공부하였다.

- ackermann steering - 일반적인 자동차의 조향 방법
- differential drive - 두 바퀴의 속도 방향 조향
- skid steering - 네 바퀴의 속도로 방향 조향
- bicycle model - 자전거 모델
- mecanum wheel - 전방향 휠

지금까지 했던 예제의 로봇은 skid steering이였는데, 이러한 모델은 제자리 회전에 약하다는 단점이 있다. (회전 최초 위치에서 벗어난다)

그래서 프로젝트에서는 제자리 회전에 강한 differential drive모델을 사용하였다.

## Description 실행

아래 명령어를 실행하 description을 실행 할 수 있다.

```bash
# skid steering model
$ ros2 launch gcamp_gazebo skidbot_description.launch.py
# differntial drive model
$ ros2 launch gcamp_gazebo diffbot_description.launch.py
```

명령어를 입력해도 Rviz가 실행되지 않았다.

오류를 해결하기 위해 방법들을 찾아봤지만 아직 해결하지 못하였다.

![Untitled](https://user-images.githubusercontent.com/80799025/180639087-7f3bc012-30d2-43f6-9699-1de046a4fe33.png)

위 예제에 막대들이 있는것을 볼 수 있는데,

이 막대들을 TF라 부른다.

로봇은 여러 파츠들로 구성되어있는데 TF는 각 파츠 사이의 변환을 도와준다.

막대들은 Tree형태의 구조를 가진다.
</br>

## Maze Escape

예제로 사용될 MazeWorld를 아래 명령어로 실행한다.

```python
$ ros2 launch gcamp_gazebo maze_world.launch.pyros2 launch gcamp_gazebo maze_world.launch.pyros2 launch gcamp_gazebo maze_world.launch.py
```

![Untitled 1](https://user-images.githubusercontent.com/80799025/180639089-da605955-3074-47c0-8cfb-25485c24fa60.png)

이 예제에서는 초록박스(탈출구) 까지 로봇을 이동시키면 성공이다.

로봇은 충돌 직전까지 직진하며, 회전방향은 남(2), 북(0,) 서(3), 동(0)으로 이동할 수 있다.

클라이언트와 서버를 아래 명령어로 실행한다.

```
$ ros2 run py_action_pkg maze_action_server
$ ros2 run py_action_pkg maze_action_client
```

서버를 실행하였는데, OpenCV가 설치되어 있지 않아 오류가 발생하였다.

다음 명령어를 입력하여 OpenCV를 설치하였다.

```python
$ sudo apt update
$ sudo apt install python3-opencv
```

방향을 입력하여 로봇이 탈출 할수 있도록 해보았다.

![Untitled 2](https://user-images.githubusercontent.com/80799025/180639093-8835892a-31f7-40da-b837-feca3b88eb3b.png)

로봇이 결승점에 도달한 것을 확인할 수 있었다.

이번 예제로 실행에 어떤것들이 필요했는지 알 수 있었다.

- 지속적으로 로봇의 이동 동향을 알려주기 ⇒ Action
- 특정 방향으로 로봇을 회전 ⇒ Odom
- 충돌 전까지 로봇을 직진 ⇒ LaserScan & Twist
- 초록 박스를 인식 ⇒ Image

등이 있다.
</br>

## Image sub

로봇 전방에 달린 카메라 영상을 다루어 보았다.

```bash
# Gazebo를 실행시킨 상태에서
$ ros2 run image_view image_view --ros-args --remap /image:=/diffbot/camera_sensor/image_raw
```

위 명령어 실행시 image_view가 설치되지 않았다는 오류가 발생한다.

image_view를 설치해도 제대로 적용되지 않아 show image를 이용하였다.

```bash
$ ros2 run image_tools showimage --ros-args --remap /image:=/diffbot/camera_sensor/image_raw
```

![Untitled 3](https://user-images.githubusercontent.com/80799025/180639097-fd442655-8ad8-4398-a78b-282abd4bbca6.png)

다음과 같이 로봇의 시점을 볼 수 있었다.
</br>

ROS2는 이미지를 다루기 위한 msg 형식을 갖고있다.

 OpenCV의 형식을 ROS2의 형식으로 바꾸기 위해 `cv_bridge를`를 사용한다.

코드는 다음과 같다.

```python
# !/usr/bin/env/ python3
#
# Basic ROS 2 program to publish real-time streaming 
# video from your built-in webcam
# Author:
# - Addison Sears-Collins
# - https://automaticaddison.com

# opencv 모듈 삽입
import rclpy

from rclpy.node import Node
# cv_bridge
from cv_bridge import (
    CvBridge,
    CvBridgeError,
)  # Package to convert between ROS and OpenCV Images

import rclpy
from rclpy.node import Node
# ROS2의 image 형식
from sensor_msgs.msg import Image  # Image is the message type

class ImageSubscriber(Node):
    """
    Create an ImageSubscriber class, which is a subclass of the Node class.
    """

    def __init__(self):
        """
        Class constructor to set up the node
        """
        super().__init__("image_subscriber")
        self.sub_period = 10  # Hz

        # topic subscriber를 생성
        self.subscription = self.**create_subscription**(
            Image,
            "/diffbot/camera_sensor/image_raw",
            self.listener_callback,
            self.sub_period,
        )
        self.subscription

        # ROS2 <=> OpenCV를 해주는 cv_bridge 
        self.cv_bridge = CvBridge()

    def listener_callback(self, data):
				# 변환
        try:
						# OpenCV에서 사용하는 bgr8로 사용
            current_frame = **self.cv_bridge.imgmsg_to_cv2**(data, "bgr8")
        except CvBridgeError as e:
            self.get_logger().info(e)

        #Display image
        cv2.imshow("camera", current_frame)
        cv2.waitKey(1)

				# image의 정 가운데 pixel을 가져온다
        self.center_pixel = current_frame[400, 400]

def main(args=None):

    rclpy.init(args=args)

    image_subscriber = ImageSubscriber()

    rclpy.spin(image_subscriber)

    image_subscriber.destroy_node()

    rclpy.shutdown()

if __name__ == "__main__":
    main()
```
</br>

## Odom sub

미로 예제를 실행하면서 로봇이 회전할때마다 약간씩 오차가 발생하는것을 볼 수 있었다.

이는 각속도를 이용하여 로봇을 회전시켰기 때문이다.

오차를 줄이기 위해 Odom이 등장하였는데, Gazebo시뮬레이션 안에서 로봇의 절대적인 위치,방향을 알 수 있다.

데이터는  `/odom`  topic안에 담겨있다.

하지만 Odom의 자료형을 보면 `quaternion` 으로 되어있어  `euler angle`로 바꿔줘야 한다.

아래 명령어를 통해 publish되고있는 odm topic을 찾았다.

```cpp
$ ros2 topic list
```

![Untitled 4](https://user-images.githubusercontent.com/80799025/180639104-7eb51b6f-c32b-43be-810a-7a7ac6812b92.png)

토픽을 확인해본 결과 각도에 관한 값들이 4개의 변수로 이루어져 있는것을 볼 수 있다.

이를 사용하기 위해 오일러 각으로 변환시키는 코드를 이용하였다.

```python
#!/usr/bin/env/ python3
#
# Copyright 2021 Seoul Business Agency Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cv2

# Odometry는 nav_msgs안에 있다.
from nav_msgs.msg import Odometry  # Odometry is the message type
import numpy as np
import rclpy
from rclpy.node import Node

# quaternion를 euler angle로 함수
def euler_from_quaternion(quaternion):
    """
    Converts quaternion (w in last place) to euler roll, pitch, yaw
    quaternion = [x, y, z, w]
    Bellow should be replaced when porting for ROS 2 Python tf_conversions is done.
    """
    x = quaternion.x
    y = quaternion.y
    z = quaternion.z
    w = quaternion.w

    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = np.arctan2(sinr_cosp, cosr_cosp)

    sinp = 2 * (w * y - z * x)
    pitch = np.arcsin(sinp)

    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = np.arctan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw

class OdometrySubscriber(Node):
    """
    Create an OdometrySubscriber class, which is a subclass of the Node class.
    """

    def __init__(self):
        """
        Class constructor to set up the node
        """
        # Initiate the Node class's constructor and give it a name
        super().__init__("odom_subscriber")
        self.sub_period = 10  # Hz

				# 로봇으로부터의 odom subscribe
        self.subscription = self.create_subscription(
            Odometry,
            "diffbot/odom",
            self.listener_callback,
            self.sub_period,
        )
        self.subscription  # prevent unused variable warning
			# listener_callback
    def listener_callback(self, data):
		    orientation = data.pose.pose.orientation
        _, _, self._yaw = euler_from_quaternion(orientation)
			# 로그 출력
				self.get_logger().info(f"Current Yaw Angle : {self._yaw}")

def main(args=None):

    rclpy.init(args=args)

    Odometry_subscriber = OdometrySubscriber()

    rclpy.spin(Odometry_subscriber)

    Odometry_subscriber.destroy_node()

    rclpy.shutdown()

if __name__ == "__main__":
    main()
```

아래 명령어를 이용해 노드를 실행하여 결과를 확인해 보았다.

```bash
$ ros2 run py_action_pkg odom_sub_node
```

![Untitled 5](https://user-images.githubusercontent.com/80799025/180639110-dc1ff83d-8952-4d3b-a136-4dd8b903d448.png)

다음과 같이 실시간으로 현재 각을 출력한다.
