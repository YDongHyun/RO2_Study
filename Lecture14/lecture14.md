# ROS2_Study Lecture14

# Service 프로래밍 - C++

전 강의에서는 Python을 통해 Service를 프로그래밍 하였고, 이번에는 C++을 이용하여 진행하였다.

먼저 아래 예제를 통해 패키를 빌드하고 실행해보았다

```bash
$ cbp cpp_service_pkg

$ ros2 launch gcamp_gazebo gcamp_world.launch.py

#terminal 2
$ ros2 run cpp_service_pkg robot_turning_server_node
#terminal 3
$ ros2 run cpp_service_pkg robot_turning_client_node 5 0.5 1.0
```

terminal3에 입력한 마지막 숫자는 duration,linear, angular이다.

다음을 실행한 결과 5초간 로봇이 전진 회전을 하였다.

## Service  Server구현

먼저 위 예제에서 사용된 src타입을 알아보았다.

![Untitled](https://user-images.githubusercontent.com/80799025/179472318-35a4aea2-4d99-4de2-b818-174cc22d4766.png)

다음과 같이 time_durtion, angular, linear라는 값을 받는것을 볼 수 있다.

위 Sevice의 코드를 살펴보았다.
</br>

**robot_turning_server**

```cpp
// Copyright 2021 Seoul Business Agency Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// 헤더파일
#include <memory>
#include "custom_interfaces/srv/turning_control.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"

//using keyword를 사용하여 긴 코드를 간결화
using Twist = geometry_msgs::msg::Twist;
using TurningControl = custom_interfaces::srv::TurningControl;

//클래스 선언
class RobotTurnServer : public rclcpp::Node {
private:
  rclcpp::Service<TurningControl>::SharedPtr m_service;
  rclcpp::Publisher<Twist>::SharedPtr m_twist_pub;

  Twist m_twist_msg;

public:
  RobotTurnServer() : Node("robot_turn_server") {
    RCLCPP_WARN(get_logger(), "Robot Turn Server Started");

    m_twist_pub = create_publisher<Twist>("skidbot/cmd_vel", 10);
//service생성
//TurningControl -> 사용할 srv타입
//turn_robot -> service이름
//std::bind -> request시 실행될 callback
//매개변수를 2개 받으로 placeholders::_1, _2 두개를 입력한다.
    m_service = create_service<TurningControl>(
        "turn_robot", std::bind(&RobotTurnServer::response_callback, this,
                                std::placeholders::_1, std::placeholders::_2));
  }

  // uint32 time_duration
  // float64 angular_vel_z
  // float64 linear_vel_x
  // ---
  // bool success

  void response_callback(std::shared_ptr<TurningControl::Request> request,
                         std::shared_ptr<TurningControl::Response> response) {
    auto t_start = now();
    auto t_now = now();
//시간이 nanoseconds이기 때문에 1초는 1e9가 된다
    auto t_delta = request->time_duration * 1e9;

    RCLCPP_INFO(get_logger(), "\nTime Duration : %d\nLinear X Cmd : %f\nAngular Z Cmd : %f",
      request->time_duration, request->linear_vel_x, request->angular_vel_z);

    RCLCPP_INFO(get_logger(), "Request Received Robot Starts to Move");

    while ((t_now - t_start).nanoseconds() < t_delta) {
      t_now = now();
      move_robot(request->linear_vel_x, request->angular_vel_z);
    }
    stop_robot();

    RCLCPP_WARN(get_logger(), "Request Done Wating for next request...");
    response->success = true;
  }

//받은 변수를 통해 로봇이 움직일 방향 결정
  void move_robot(const float &linear_x, const float &angular_z) {
    m_twist_msg.linear.x = linear_x;
    m_twist_msg.angular.z = angular_z;

    m_twist_pub->publish(m_twist_msg);
  }
//로봇 정지
  void stop_robot() {
    m_twist_msg.linear.x = 0.0;
    m_twist_msg.angular.z = 0.0;
    m_twist_pub->publish(m_twist_msg);

    RCLCPP_INFO(get_logger(), "Stop Robot and make Node FREE!");
  }
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);

  auto node = std::make_shared<RobotTurnServer>();

//rclcpp spin사용하여 request받고 response보내는 부분을 스케줄링
  rclcpp::spin(node);
  rclcpp::shutdown();
}
```

코드분석을 해보았지만 아직 부족한거 같다.

관련 공부를 더 해봐야겠다.

## Service Client 구현

Client부의 코드를 분석하였다.
</br>

**robot_turning_client**

```cpp
// Copyright 2021 Seoul Business Agency Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

//헤더 선언
#include <chrono>
#include <cstdlib>
#include <memory>

#include "custom_interfaces/srv/turning_control.hpp"
#include "rclcpp/rclcpp.hpp"

//using을 사용하여 축약
using namespace std::chrono_literals;
using TurningControl = custom_interfaces::srv::TurningControl;

class RobotTurnClient : public rclcpp::Node
{
private:
//service 클라이언트 선언
//std rclcpp 다르므로 주의
  rclcpp::Client<TurningControl>::SharedPtr m_client;
  std::shared_ptr<TurningControl::Request> m_request;

public:
  RobotTurnClient() : Node("robot_turn_client")
  {
	//클라이언트 생성
	//클라이언트 생성시 사용하는 srv타입, request할 service이름을 받음
    m_client = create_client<TurningControl>("turn_robot");
    m_request = std::make_shared<TurningControl::Request>();
	//requset할 server가 없으면 기다림
    while (!m_client->wait_for_service(1s))
      RCLCPP_INFO(get_logger(), "service not available, waiting again...");

    RCLCPP_INFO(get_logger(), "service available, waiting serice call");
  }

  // uint32 time_duration
  // float64 angular_vel_z
  // float64 linear_vel_x
  // ---
  // bool success
	//requset를 보내 future를 반환받는다.
  auto get_result_future(const int &time_in, const float &linear_x_in,
                         const float &angular_z_in)
  {
    RCLCPP_WARN(get_logger(), "Input Info");
    RCLCPP_INFO(get_logger(), "time_duration : %d\nlinear_vel_x : %f\nangular_vel_z : %f",
      time_in, linear_x_in, angular_z_in);

    m_request->time_duration = time_in;
    m_request->linear_vel_x = linear_x_in;
    m_request->angular_vel_z = angular_z_in;
	
	//async는 비동기
    return m_client->async_send_request(m_request);
  }
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
	//argc가 4일 경우 예외처리
  if (argc != 4)
  {
    RCLCPP_INFO(
        rclcpp::get_logger("rclcpp"),
        "usage: robot_turning_client [seconds] [linear_vel_x] [angular_vel_z]");
    return 1;
  }
	
  auto basic_service_client = std::make_shared<RobotTurnClient>();
	//atoi는 int형으로,atof는 float형으로 변환해준다.
  auto result = basic_service_client->get_result_future(
      atoi(argv[1]), atof(argv[2]), atof(argv[3]));

  // Wait for the result.
	//spin을 유지하여 result를 기다린다
  if (rclcpp::spin_until_future_complete(basic_service_client, result) ==
      rclcpp::executor::FutureReturnCode::SUCCESS)
    RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Result : %s",
                result.get()->success ? "True" : "False");
  else
    RCLCPP_ERROR(rclcpp::get_logger("rclcpp"),
                 "Failed to call service add_two_ints");

  rclcpp::shutdown();
  return 0;
}
```
</br>

**비동기** 

위 코드에서 잠시 나왔던  **async**는 비동기라 한다.

비동기란**ynchronous service clientynchronous service client**

response 시간이 필요한 service request 동안 다른 일을 하다가, response가 오는 시점에 다시 돌아와 그 결과받는 일처리 방식을 말한다.

만약 앞선 일처리가 끝난 후 다음 일을 수행하고 싶다면  **synchronous service client**를 이용한다.

main함수에 나왔던 `spin_until_future_complete` 를 살펴보았다.

```cpp
if (rclcpp::spin_until_future_complete(basic_service_client, result) ==
      rclcpp::executor::FutureReturnCode::SUCCESS)
```

위 함수는 input, output을 받는다.

input으로 future와 해당 future가 속한 node를 받고,

output으로 result를 받는다.
