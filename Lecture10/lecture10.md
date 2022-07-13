# ROS2_Study Lecture10

# Node 프로그래밍 C++

저번 강의에서는 Python을 이용하였고, 이번 예제에서는 C++을 이용하여 프로그래밍

## 예제 실행

```bash
$ rosfoxy
$ cbp cpp_first_pkg #C++
```

다음 예제들이 모두 실행되는지 확인

```bash
# New Terminal 
$ ros2 run cpp_first_pkg simple_node

$ ros2 run cpp_first_pkg simple_loop_node

$ ros2 run cpp_first_pkg simple_oop_node

$ ros2 run cpp_first_pkg lifecycle_node #Ctrl+C까지 확인
```

모든 예제들이 정상적으로 실행됨을 확인하였다.

예제 명령어의 역할을 정의하면 다음과 같다.

- `simple_node` :  Node의 생성 후 Log를 출력하는 예제
- `simple_loop_node` : Node의 생성 후 주기적으로 Log를 출력하는 예제
- `simple_oop_node` :  상속을 통한 Node 생성

C++ 코드를 살펴보기 위해 Vscode를 이용하였다.

![Untitled](ROS2_Study%20Lecture10%20f60b26e9463f470682fc918e6e20dc53/Untitled.png)

다음과 같이 코드들을 확인고 수정할 수 있다.

## Node 생성

Node생성을 살펴보기 위해 simple.cpp파일을 확인였다.

모든 Node는 포인터 형식을 갖고 있음에 주의한다.

```cpp
#include "rclcpp/rclcpp.hpp"

int main(int argc, char **argv) {
	//rclcpp을 초기화
  rclcpp::init(argc, argv);
	//Node의 생성은 Node::make_shard 로 생성, 괄호에 노드 이름
	//std가 아닌 rclcpp 사용.
  auto node = rclcpp::Node::make_shared("simple_node");

  RCLCPP_INFO(node->get_logger(), "Logger Test");
	
//ros2 종료
  rclcpp::shutdown();
  return 0;
}
```

## Node 동작

주기적인 동작을 위해 timer사용

rclcpp::WallRate 와 rclcpp::Rate가 사용된다.

WallRate는 steady_clock기반 →단순히 계속 늘어나는 시간

Rate는 system_clock 기반 → 시스템 부하시 오차 발생

따라서  WallRate방식을 추천

## **Node Composition**

C++의 객체지향

만일 클래스 안의 함수를 일반함수처럼 사용하고 싶다면 `std::bind`를 사용

EX)

```cpp
std::bind(&Talker::timer_callback, this);
```

따라서 함수가 어떤 형태의 객체 내의 함수인지, 몇개의 매개변수를 받는지가 중요

## Spin

While 루프대신에 사용할 수 있다.

`rclcpp::spin`=  무한 루프 (파이썬의 spin)

`rclcpp::spin_some`= 한번 반복 (파이썬의 spin_once)

또한 `rclcpp::spin` 을 사용하면 이 노드가 얼마의 주기로 실행되는 확인

따라서 class안에 timer선언

```cpp
class Talker : public rclcpp::Node
{
private:
	//타이머 선언
  rclcpp::TimerBase::SharedPtr m_timer;
	...

public:
  Talker() : Node("simple_oop_node")
  {
    m_timer = this->create_wall_timer(std::chrono::milliseconds(500), std::bind(&Talker::timer_callback, this));
  }
};
```

## Node & rclcpp - lifecycle

`lifecycle_node` : Node가 생성되고 소멸되는 시점과 rclcpp이 시작되고 종료되는 시점

```cpp
#include <memory>
#include "rclcpp/rclcpp.hpp"

class Talker : public rclcpp::Node
{
private:
  rclcpp::TimerBase::SharedPtr m_timer;
  size_t m_count;

  void timer_callback()
  {
    m_count++;
		// spin이 Node를 주기적으로 동작시키는 지점 확인
    RCLCPP_INFO(this->get_logger(), "I am Simple OOP Example, count : %d", m_count);
  }

public:
  Talker() : Node("simple_oop_node"), m_count(0)
  {
		// 생성자 부분에 Log
    RCLCPP_WARN(this->get_logger(), "Node Constructor");

    m_timer = this->create_wall_timer(std::chrono::milliseconds(500), std::bind(&Talker::timer_callback, this));
  }

  ~Talker(){
		// 소멸자 부분에 Log
    RCLCPP_WARN(this->get_logger(), "Node Destructor");
  }
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  
  auto talker = std::make_shared<Talker>();
  rclcpp::spin(talker);
  
	// Spin이 언제 종료되는지 확인
  RCLCPP_INFO(talker->get_logger(), "==== Spin Done ====");
  rclcpp::shutdown();

	// rclcpp이 언제 종료되는지 확인
  std::cout << "==== After Shutdown ====" << std::endl;

  return 0;
}
```

코드를 실행한 결과는 다음과 같다.

![Untitled](ROS2_Study%20Lecture10%20f60b26e9463f470682fc918e6e20dc53/Untitled%201.png)

따라서 lifecycle은 다음 순서로 진행됨을 알 수 있다.

rclcpp 실행 → Node생성 → spin → spin out(강제 종료) →rclcpp종료 → Node소멸

Node는 소멸하기 때문에 ROS통신 관련 코드는 Node소멸자에는 넣지 않도록 한다.