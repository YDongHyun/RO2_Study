# ROS2 TOPIC

## Moving Robot

아래 명령어로 패키지를 빌드

```bash
$ rosfoxy
$ cbp py_topic_pkg

# Terminal 1
$ ros2 launch gcamp_gazebo gcamp_world.launch.py

# Terminal 2
$ ros2 run py_topic_pkg cmd_vel_pub_node 
```

![Untitled](https://user-images.githubusercontent.com/80799025/177919383-3432555f-8c64-40b5-80a9-5d2b1bceb92f.png)


로봇이 5초간 회전하고 정지한다.

이러한 명령어가 어떻게 처리되었는지 그래프 보면 다음과 같다.

![Untitled 1](https://user-images.githubusercontent.com/80799025/177919467-194bc313-230a-48fe-b92a-358783969059.png)

- `cmd_vel_pub_node` 라는 새로운 node에서 로봇에게 움직이라 명령을 내리고, `skidbot/cmd_vel` 이라는 Topic을 통해 message를 전달한 것이다.

## ROS2 Topic

위 그래프에서 살펴본 것처럼, **Topic은 Node들 사이에 데이터(Message)가 오가는 길의 이름이다.**

ROS2에서  `**Publisher**`(발행자) `**Subscriber**`(구독자)로 나누어 송신, 수신자를 구분.

Topic을 통해 Message가 전달되는 것이다.

또한 Topic은 1대 다 통신이 가능하다.

하나의 publisher가 메세지를 Topic으로 보내면 2개 이상의 subscriber가 받는것이 가능
</br></br>

## Topic Message

- 로봇 프로그래밍시 다양한 센서들이 다루어 진다
- 센서 뿐 아니라 제어 데이터도 주고받아야 한다

ROS2에서 사용되는 주요 데이터 형식은 Message이며, 직접 커스터 마이징이 가능

EX) `skidbot/cmd_vel` topic은  **geometry_msgs/msg/Twist** 형식의 message를 사용

![Untitled 2](https://user-images.githubusercontent.com/80799025/177919534-c93910f7-2793-477a-8214-fb0ea2199070.png)

### message type을 선택하기 위한 방법

- 오픈소스 프로젝트를 참고
- 직접 새로운 메세지를 선언


## Topic Command

명령어를 입력하여 로봇이 계속 회전하도록 한다.

```bash
$ rosfoxy
$ ros2 run py_topic_pkg endless_cmd_vel_pub_node
```

실행중인 topic의 리스트와 특정 topic의 정보를 알고 싶을때 아래 명령어를 사용한다.

```bash
$ ros2 topic list
$ ros2 topic info /skidbot/cmd_vel
``

![Uploading Untitled 3.png…]()

다음과 같이 Topic의 리스트와, Topic의 수신자 송신자의 수를 볼 수 있다.

**특정 message가 어떻게 구성되어 있는지 알고싶을 때, 다음 커맨드를 사용**

```bash
$ ros2 interface show geometry_msgs/msg/Twist
```

![Untitled 4](https://user-images.githubusercontent.com/80799025/177919578-0f1f5d69-0187-42c3-ad7c-98f0c4374529.png)

다음과 같이 linear, angular라는 message의 유형을 볼 수 있다.
</br>

## 커맨드를 사용한 Publish

```bash
$ **ros2 topic pub** **--rate 1** /skidbot/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.0}}"
$ **ros2 topic pub --once**  /skidbot/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
```

위와 같은 커맨드로 로봇을 회전 혹은 정지시킬 수 있다.

Publish가 잘 되고있는지 확인할 때 echo 명령어를 이용한다.

```
$ ros2 topic echo /skidbot/cmd_vel
```

![Untitled 5](https://user-images.githubusercontent.com/80799025/177919596-7087355e-5316-4ca1-8e98-b443e3f9ccf8.png)

다음과 같이 현재 로봇의 값들이 어떻게 변하는지 실시간으로 확인할 수 있다.

<aside>
💡 rpt 그래프로도 다음과 같이 세부 데이터 확인이 가능하다.** 
rqt →Plugins → Topic → Topic Moniter → 체크 후 확인
하지만 이 방법은 업데이트가 느리다는 단점이 있다.rpt 그래프로도 다음과 같이 세부 데이터 확인이 가능하다.

</aside>
