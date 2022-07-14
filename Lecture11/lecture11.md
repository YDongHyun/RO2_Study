# Topic 프로그래밍 - C++

## Build & 예제실행

C++노드는 다음 명령어로 실행 가능

```bash
$ cbp cpp_topic_pkg

# Terminal 1
$ ros2 launch gcamp_gazebo gcamp_world.launch.py

# Terminal 2
$ ros2 run cpp_topic_pkg cmd_vel_pub_node
```

다음 명령어를 실행하면 파이썬의 예제와 같이 5초간 회전하고 정지한다.

C++노드 잘 작동됨을 확인였다.
</br>

## Publish Node 작성

### 코드분석

- 로봇을 움직이기 위해 topic message type을 사용하기 위해 헤더를 `include`

```cpp
#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"
```

- CammelCase : 단어 사이에 시작은 대문자
- snake_case : 모두 소문자

c++ 헤더는 파이썬과 다르 snake_case를 취한다.
</br>

### Class 내부

```cpp
class TwistPub : **public rclcpp::Node**
{
private:
	// topic publisher의 type
  rclcpp::Publisher<**geometry_msgs::msg::Twist**>::**SharedPtr** m_pub;
	// timer
  rclcpp::TimerBase::SharedPtr m_timer;

	// topic message로 geometry_msgs::msg::Twist 타입
  geometry_msgs::msg::Twist **m_twist_msg**;
	
	//call back 함수
  void timer_callback()
  {
    move_robot();
  }

public:
  TwistPub() : Node("cmd_vel_pub_node")
  {
    RCLCPP_INFO(get_logger(), "Cmd_vel Pub Node Created");
		
		//publisher 생성
    m_pub = create_publisher<geometry_msgs::msg::Twist>("skidbot/cmd_vel", 10);
		//call back 함수를 
****    m_timer = create_wall_timer(std::chrono::milliseconds(100), std::bind(&TwistPub::timer_callback, this));
  }

  void move_robot()
  {
    m_twist_msg.linear.x = 0.5;
    m_twist_msg.angular.z = 1.0;
		// m_pub은 포인터 형식, ->를 사용
    m_pub**->**publish(m_twist_msg);

    // std::cout << "==== Move Robot ====" << std::endl;
  }

  void stop_robot()
  {
    m_twist_msg.linear.x = 0.0;
    m_twist_msg.angular.z = 0.0;
    m_pub->publish(m_twist_msg);

    std::cout << "==== Stop Robot ====" << std::endl;
  }
};
```

전체적인 코드의 내용은 파이썬과 비슷하다.

하지만 C++의 문법에 아직 익숙하지 않아 다음 코드를 분석하기에 어려움이 있다.

대략적인 개요와 흐름은 이해했지만 완벽하지 못해

C++의 문법을 더 공부한 후 코드를  분석할 계획이다.


## Create_publisher

Publisher를 생성하는 것이다.Create_publisherCreate_publisherCreate_publisherCreate_publisher

publisher는 `create_publisher` 함수를 통해 생성

EX)

```cpp
m_pub = create_publisher<geometry_msgs::msg::Twist>("skidbot/cmd_vel", 10);
// <>안에 message type
// 첫번째 매개변수 생성할 Topic 이름
// 두번째 매개변수 queue size(대기열) 전달
```

## main부

```cpp
int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);

	// auto는 자동으로 추론되는 연산자 지정
  auto twist_pub = std::make_shared<TwistPub>();

	// t_start, t_now 변수에 현재 시간
  auto t_start = twist_pub->**now**();
  auto t_now = twist_pub->**now**();
main부
	auto stop_time = 5.0;

	// while문 안에 spin_some(한번반복)
  while ((t_now - t_start).**seconds**() < stop_time)
  {
    t_now = twist_pub->now();
		// t_now변수 업데이트
    twist_pub->move_robot();

		// 경과시간 출력
		RCLCPP_INFO(twist_pub->get_logger(), "%f Seconds Passed", (t_now - t_start).seconds());
  }

  twist_pub->stop_robot();

  rclcpp::shutdown();

  return 0;
}
```

main부 또한 파이썬과 전체적인 맥략은 같다.

이번 코드는 어려운 문법이 들어가지 않아 수월하게 분석할 수 있었다.

## ROS2 C++시간 API

ROS2에서 시간을 다루는 코드

main부에서 사용했듯이 now()로 현재시간을 가져올 수 있다,

seconds와 nanoseconds가 있는데, nanoseconds는 seconds*1e9 이다,

## **Laser Scan Subscriber 예제**

파이썬에서 배웠던 내용과 같다.

전방 180도를 스캔하는 레이더에 대한 코드이다.

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

#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"

using LaserScan = sensor_msgs::msg::LaserScan;

//class 선언
class LaserSub : public rclcpp::Node {
private:
  rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr m_sub;

public:
  LaserSub() : Node("topic_sub_oop_node") {
		//subsciber를 생성
		//timer 사용시 std::bind로 가져온다
    m_sub = this->create_subscription<sensor_msgs::msg::LaserScan>(
        "skidbot/scan", 10,
        std::bind(&LaserSub::sub_callback, this, std::placeholders::_1));
  }
		//subscibe마다 callback 함수가 실행
  void sub_callback(const sensor_msgs::msg::LaserScan::SharedPtr msg) {
    // std::cout << (msg->ranges).size() << std::endl;

    // for (auto e : msg->ranges)
    //   std::cout << e << std::endl;

    RCLCPP_INFO(this->get_logger(), "Distance from Front Object : %f", (msg->ranges)[360]);
  }
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
	//spin을 통한 갱신
  rclcpp::spin(std::make_shared<LaserSub>());
  rclcpp::shutdown();

  return 0;
}
```

또한 긴 message type을 `using`을 통해 손쉽게 사용 가능하다.

EX)

```cpp
using LaserScan = sensor_msgs::msg::LaserScan;
```


## create_subscription

`create_subscription` 함수로 subscription을 생성

```cpp
 m_sub = this->create_subscription<sensor_msgs::msg::LaserScan>(
        "skidbot/scan", 10,
        std::bind(&LaserSub::sub_callback, this, std::placeholders::_1));
  }
// <>안에 message type
// 첫번째 매개변수 생성할 Topic 이름
// 두번째 매개변수 queue size(대기열) 전달
// 세번째 매개변수 std::bind를 통해 callback함수를 전달
// callback함수의 매개변수가 1개이므로, std::placeholders::_1이 사용ranges 배열이 기존 Python에서는 list 형식으로 표현되었지만, C++에서는 vector로 표현된다는 점에서 차이가 있습니다.
```


## Packing Example

파이썬에서 실습해보았던 주차 예제이다.

packing.cpp파일의 중요한 로직을 살펴보았다.

```cpp
  void sub_callback(const LaserScan::SharedPtr msg)
  {
		//360으로 전방의 거리를 받음
    auto forward_distance = (msg->ranges)[360];
		//거리 0.8초과면 로봇 전진
		if (forward_distance > 0.8) {
      move_robot(forward_distance);
    } else {
      stop_robot();
      rclcpp::shutdown();
    }
  }
```

이번 코드는 쉽게 해석이 되었다.

![Untitled](https://user-images.githubusercontent.com/80799025/178928817-2a2cdf13-4202-412b-b1f7-5d72dd3f7af5.png)

이를 실제 실행해 보았고, distance가 0.8에 가까워지자 정지하였다.
