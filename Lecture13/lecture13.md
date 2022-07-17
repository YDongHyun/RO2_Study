# Service 프로그래밍 - Python

## Service Client 작성

12강에 했던 빨간 로봇을 등장시키는 client

이 client의 srv타입은 다음과 같다.

![Untitled](https://user-images.githubusercontent.com/80799025/179396591-72388179-b807-4d14-9a1a-74d493dc975a.png)

Class 내부를 분석해 보았다.

```python
class SpawnRobot(Node):

    def __init__(self):
        super().__init__("gazebo_model_spawner")
				# Service Client 생성
        self.client = self.**create_client**(SpawnEntity, "/spawn_entity")

				# 잘못된 service이름을 호출면 무한정 기다림
				# 이를 방지하기 위해 최대로 Server를 기다릴 시간을 지정
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().error("service not available, waiting again...")

				# 로봇 파일 접근
        # Get urdf path  절대 경로합니다.합니다.
        self.urdf_file_path = os.path.join(
				# get_package_share_directory를 통해 패키지의 파일시스템에 접근
            get_package_share_directory("gcamp_gazebo"),
            "urdf",
            "skidbot2.urdf",
        )

				# request선언, Topic과 달리 service는 request만을 받는다.
        self.req = SpawnEntity.Request()
```

### create_client

`create_client`Service Client를 생성할 시 필요한 매개변수

- `SpawnEntity` : 사용할 srv 타입
- `/spawn_entity` : request를 보낼 Service 이름

이번에는 request부분을 분석해 보았다.

```python
    def send_req(self):
				# 앞서 선언한 urdf 파일도 전달 
        self.req.name = "skidbot2"
        self.req.xml = open(self.urdf_file_path, "r").read()
				#namespace를 지정하여 지정된 로봇에게 명령어를 하달할수 있게 한다.
        self.req.robot_namespace = "skidbot2"
				#로봇의 최초 위치 지정 (z=0.0일때 땅에 박히는 경우가 있음)
        self.req.initial_pose.position.x = 1.0
        self.req.initial_pose.position.y = 1.0
        self.req.initial_pose.position.z = 0.3

				# request call 이후 상태를 반환하는 future를 예약
        print("==== Sending service request to `/spawn_entity` ====")
        self.future = self.client.call_async(self.req)

        return self.future
```

**future**

위 코드에 future라는 생소한 표현이 나온다.

future는 특정 작업에 대해 작업이 완료될 것임을 약속한 것이다.

```python
    #robot_spawn_node.send_req()는 반드시 끝날 것을 보장
		future = robot_spawn_node.send_req()
		#그동안 robot_spawn_node를  반복
    rclpy.**spin_until_future_complete**(robot_spawn_node, future)
```

main 내부 분석

```python
def main(args=None):

    rclpy.init(args=args)

    robot_spawn_node = SpawnRobot()
		# robot_spawn_node으로부터 request call이 완료될 것임을 약속
    future = robot_spawn_node.send_req()

		# 약속이 지켜질 때까지 node spin
    rclpy.spin_until_future_complete(robot_spawn_node, future)

		# request call, response가 끝, future는 response를 담고 있다
    if future.done():
				# result가 제대로 전달되는지의 여부에 따라 예외 처리
        try:
            response = future.result()
        except Exception as e:
            raise RuntimeError(
                "exception while calling service: %r" % future.exception()
            )
        else:
						# 정상적으로 response가 도착했다는 로그를 출력
						robot_spawn_node.get_logger().info('==== Service Call Done ====')
            robot_spawn_node.get_logger().info(f'Status_message : {response.status_message}')
        finally:
            robot_spawn_node.get_logger().warn("==== Shutting down node. ====")
            robot_spawn_node.destroy_node()
            rclpy.shutdown()
```

## Turining Server Client

Service를 이용하여 로봇 움직이기

아래 명령어를 통해 입력된 시간, 각도, 속도대로 움직이게 할 수 있다.

```bash
# Terminal 1
$ rosfoxy 
$ ros2 launch gcamp_gazebo gcamp_world.launch.py

# Terminal 2 Service Server
$ rosfoxy
$ ros2 run py_service_pkg robot_turning_server

# Terminal 3 Service Client Call
$ rosfoxy
$ ros2 run py_service_pkg robot_turning_client
```

![Untitled 1](https://user-images.githubusercontent.com/80799025/179396598-9a7ab6c2-9803-4153-96ca-b00a849a068e.png)

다음과 같이 입력을 받아 로봇을 움직이고, 결과를 출력한다

이 예제에서 더 나아가 서비스의 특성을 알아 볼 수 있다.

## 서비스의 특성

위 클라이언트를 2개 실행하면

첫번째 클라이언트가 끝날 때 까지 2번째 클라이언트는 기다린 후 움직인다.

![Untitled 2](https://user-images.githubusercontent.com/80799025/179396602-2c003faf-af0a-4e36-b1ee-ca4c9b8c3562.png)

다음과 같이 위 터미널에서는 5초, 아래 터미널에는 1초라는 duration을 입력하였다.

이때 로봇은 위 터미널의 명령어대로 5초간 움직인 후, 바로 다음 명령어인 아래 터미널의 명령어를 실행하였다.

따라서 Service의 특성으로 작업이 끝날때까지 다음작업은 기다리게 된다는 것이다.

</br>
이번에는 위 Service의 코드를 분석해보았다.

```python
from custom_interfaces.srv import TurningControl
		...

    def send_request(self):

        while True:
            try:
								# python input을 사용하여 변수를 받는다
                td = input("> Type turning time duration: ")
                vel_x = input("> Type turning linear velocity: ")
                vel_z = input("> Type turning angular velocity: ")

								# 속도가 너무 높으면 오류를 유발할 수 있기에 예외처리
                if float(vel_z) > 1.5707 or float(vel_x) > 3:
                    raise ArithmeticError("Velocity too high !!")
								
								# 입력 데이터를 각 요소에 맞도록 데이터 형식 변환
                self.req.time_duration = int(td)

                self.req.linear_vel_x = float(vel_x)
                self.req.angular_vel_z = float(vel_z)
                break
								#에러 예외처리robot_turn_server.destroy_node()
            except ArithmeticError as e:
                self.get_logger().warn(e)
            except Exception as e:
                self.get_logger().warn(e)
                self.get_logger().warn('Not a number, PLZ Type number Again')

				# all_async의 output인 future를 반환
        self.future = self.client.call_async(self.req)
        print(
            f"linear_x : {self.req.linear_vel_x} / angular_z : {self.req.angular_vel_z}"
        )
        self.get_logger().info(" Request Sended ")
        return self.future
```

전체적인 코드는 SpawnRobot코드와 크게 차이나지 않았다.

같은 틀 안에서 다음과 같은 함수로 로봇이 입력을 받아 움직이도록 하였다.

## Service Server작성

Server는 request가 오면 처리하고 respones, 다음 request기다린다.

예제를 통해 service를 생성하는 과정을 살펴보았다.

**Service생성**

```python
				self.srv = self.create_service(
            TurningControl, "turn_robot", self.robot_turn_callback
        )
		#사용되는 srv타입, service이름, request가 들어올때마다 실행된 callback을 변수로 받음
```

**robot_turn_callback**

```python
		def robot_turn_callback(self, request, response):
				# 현재 시간을 저장 저장된 시간만큼 로봇 회전
        self.start_time = self.get_clock().now().to_msg().sec

				# move_robot은 topic과 동일
        self.move_robot(
            request.time_duration, request.linear_vel_x, request.angular_vel_z
        )
        self.stop_robot()
			
				# response를 채운다
        response.success = True
        self.get_logger().info("Servie Process Done...")

        return response
```

**main**

```python
#main부는 상시spin을 하여 새로운 requset를 처리하고 기다림을 반복한다.
def main(args=None):
    rclpy.init(args=args)

    robot_turn_server = RobotTurnServer()

    rclpy.spin(robot_turn_server)

    robot_turn_server.destroy_node()
    rclpy.shutdown()robot_turn_server.destroy_node()robot_turn_server.destroy_node()
```
