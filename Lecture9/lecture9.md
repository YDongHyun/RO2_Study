# ROS2_Study Lecture9

# Subscriber Node 작성

저번 강의에서는 Publisher Node를 만들었고 이번에는 Subscriber Node 를 만든다

### **2D Lidar**

2D Lidar는 빛이 부딪혀 돌아오는 시간을 계산하여 거리를 알 수 있다.

2차원 상으로 표현 

Laser Scan Subscriber 예제

예제 실행

```bash
$ rosfoxy
$ ros2 run py_topic_pkg laser_raw_node
```

터미널에 출력되는 숫자들은 2D Lidar의 raw(거리)데이터

![Untitled](ROS2_Study%20Lecture9%20a89a562e8f634b9b92584600211b63d9/Untitled.png)

실질적으로 숫자만 보고 알아보기 힘들다

## R**viz**

---

ROS Visualization

Rviz를 통해 Lidar의 결과를 시각화 할 수 있다.

Lidar data를 렌더링

이번에 다음 코드를 분석한다.

main부분의 코드는 Publisher부분과 동일하므로 생략

```python
# 2D Lidar는 sensor_msgs/msg/LaserScan 형식 사용
**from sensor_msgs.msg import LaserScan**

class LaserSubscriber(Node):

    def __init__(self):
        super().__init__("laser_sub_node")
        queue_size = 10
				self.subscriber = self.**create_subscription**(
            LaserScan, 'skidbot/scan', self.sub_callback, queue_size
        )
        self.subscriber # prevent unused variable warning

		# Topic을 통해 subscribe 할 때마다 이 함수가 실행
		# 그리고 두번째 매개변수인 msg에는 전달받은 Message가 담겨 있습니다.
    def **sub_callback**(self, msg):
																				#ranges = 모든 거리 데이터
				self.get_logger().info(f'Raw Laser Data : {msg.ranges}')
```

## create_subscription

---

- `LaserScan` : Topic 통신에 사용될 Message Type
- `"skidbot/scan"` : 데이터를 Subscribe받을 Topic의 이름을 지정
- `self.sub_callback` : callback 함수
- `queue_size` : 대기열의 크기

### LaserScan Message

저번 강의에서 본 것과 같이 Type를 확인

![Untitled](ROS2_Study%20Lecture9%20a89a562e8f634b9b92584600211b63d9/Untitled%201.png)

다음과 같이 많은 메세지 타입을 가진다.

실제로 Lidar에서 사용하는 것은  ranges 이다.

![Untitled](ROS2_Study%20Lecture9%20a89a562e8f634b9b92584600211b63d9/Untitled%202.png)

ranges는 전방 180도 부근을 720등분 하여 scan된 물체의 거리를 저장한다.

만약 전방이나 특정 방향의 거리만 필요하다면 다음과 같이 표현 할 수 있다.

```python
		def sub_callback(self, msg):
				#360은 전방부분을 의미
        print(f'Distance from Front Object : {msg.ranges[360]}')
```

과제로 전진하는 로봇이 벽을 만나면 정지하도록 코드를 수정하였다.

```python
	$ rosfoxy
	$ ros2 run py_topic_pkg parking_node
```

![Untitled](ROS2_Study%20Lecture9%20a89a562e8f634b9b92584600211b63d9/Untitled%203.png)

다음과 같이 로봇이 벽이 만나면 정지하였다.

#값 형식이 float 이므로 소수점 이하 자리까지 표현