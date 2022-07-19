# ROS2_Study Lecture15

# ROS2 Action

## Action의 개념

- Action client는 server가 response를 보내기 전까지 다른 일을 할 수 있다.
- Action client는 requset를 보낸 뒤 지속적으로 feedback받을 수 있다.
- feedback을 받는 도중 cancel 가능하다.

동시 여러 request작업은 불가능, 하지만 `MultiThreadedExecutor`를 이용하여 해결 가능하다.

![Untitled](ROS2_Study%20Lecture15%204c158926cdd44ae38c2f47f523ee8096/Untitled.png)

image from : [https://docs.ros.org/en/foxy/Tutorials/Understanding-ROS2-Actions.html](https://docs.ros.org/en/foxy/Tutorials/Understanding-ROS2-Actions.html)

다음 ROS2공식 이미지를 보면 복잡하게 보인다.

어떻게 작동되는지 정리하면

- client → Server, Goal Requset
- server→client, Goal Request
- client → server, Result Request
- server→client, Feedback Topic
- server → client, Result Service

다음과 같이 크게 5가지의 경로가 있다.

직관적인 이해가 어려워 예시로 이해하였다.

EX)

Action을 네비게이션이라 이해하고, 목적지를 Request받아 경로탐색, 운전 중간 FeedBack, 도착시 Requset한다.

실제 Nav2라는 ROS2 자율주행 프로젝트가 있는데, 이 프로젝트에서 Action이 많이 사용됨을 확인 할 수 있었다.

## 피보나치 수열 예제

아래 명령어를 입력하여 예제를 실행한다.

```bash
$ cbp py_action_pkg

# New Terminal
$ ros2 run py_action_pkg fibonacci_action_server

# New Terminal
$ ros2 run py_action_pkg fibonacci_action_client
```

![Untitled](ROS2_Study%20Lecture15%204c158926cdd44ae38c2f47f523ee8096/Untitled%201.png)

 Server가  Request를 받을 때 까지 대기하였다가, client로 부터 Goal Request를 받자 작동하였다.

그리고 실행하면서 중간중간 FeedBack을 보내는 것을 볼 수 있었다.

위 예제에서 사용한 예제의 데이터 타입은 action타입이다.

**Fibonacci.action**

```bash
# Goal
int32 order
---
# Result
int32[] sequence
---
# Feedback
int32[] partial_sequence
```

Topic의 msg, Service의 srv처럼 데이터 타입을 가지고 있는데,

Action의 경우에는 Goal, Result, Feedback 이렇게 3분류로 받는다.

## ROS2 Action Commands

Action을 다루기 위한 명령어를 알아보았다.

```bash
$  ros2 run py_action_pkg fibonacci_action_server

# 실행중인 Action을 확인
$ ros2 action list

# 특정 Action의 정보 조회
$ ros2 action info /fibonacci

# Action타입의 상세정보 조회
$ ros2 interface show custom_interfaces/action/Fibonacci
```

또한 Action Server에게 Client 프로그래밍 없이 바로 Goal Requset가 가능하다.

```bash
# Goal Requset 방법
$ ros2 action send_goal <Action-name> <action-type> {actual: value}

# Goal Requset 예제 실행
*$ ros2 action send_goal fibonacci custom_interfaces/action/Fibonacci "{order: 5}"*
```

![Untitled](ROS2_Study%20Lecture15%204c158926cdd44ae38c2f47f523ee8096/Untitled%202.png)

다음과 같이 order 5만큼이 실행 되었다.

만약 FeedBack을 같이 출력하고 싶다면 아래 명령어로 가능하다.

```bash
$ ros2 action send_goal --feedback fibonacci custom_interfaces/action/Fibonacci "{order: 5}"
```

![Untitled](ROS2_Study%20Lecture15%204c158926cdd44ae38c2f47f523ee8096/Untitled%203.png)

전과 달리 실행되면서 FeedBack을 내보내고 있음을 볼 수 있다.

## Goal Cancel

Action은 Requset이후에 FeedBack을 받다 Cancel시키는것이 가능하다.

```bash
# Server Cancel
$ ros2 run py_action_pkg fibonacci_action_server_cancel
# Client Cancel
$ ros2 run py_action_pkg fibonacci_action_client_cancel
```

위 예제는 일정시간이 지나면 Cancel되도록 프로그래밍 되있다.

다르게 프로그래밍하면 특정 값이 나오거나 값을 바꿀경우 Cancel되도록 할 수 있을것이다.이런 방식이 아니라, Feedback에 따라서 Cancel의 요청 여부를 결정지을 수도 있겠지요.