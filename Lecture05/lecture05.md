# ROS2  Node, Package와 기본 커맨드


## Node란?


 로봇 개발을 위해 로봇을 구성하는 여러 센서들, 센서 데이터를 통해 지속적으로 판단하고 동작해야는 시스템 필요

 EX) 카메라를 통한 표지판 인식

 카메라 센서로부터 이미지get → 이미지 판단 → 판단 결과로 제어

 ![Untitled](https://user-images.githubusercontent.com/80799025/177294910-a7da2a9b-fc91-4873-8c5f-34125834b48a.png)

 노드사이에 서로 데이터를 주고받는 구조가 된다.


### Topice, Service, Action


 Node 사이의 의사소통 방법 (데이터 주고받기)

 각각의 방식마다 특징과 장단점을 가짐

## ROS2 Node 커맨드 라인



### Node의 실행


 단일 노드의 실행은  `ros2 run`로 확인

 전에 설치해둔 turtlesim을 이용하였다.

```bash
$ rosfoxy
$ ros2 run turtlesim turtlesim_node
```

 노드를 선택하여 실행하였다.
  </br>
 </br>
### 실행중인 Node들의 리스트 확인



 특정 Node의 정보 살펴보기

 저번시간에 설치한 Gazebo 예제를 실행하였다.

 그후 다음과 같은 명령어를 입력

```bash
$ ros2 launch gcamp_gazebo gcamp_world.launch.py
$ ros2 node list
```

 ![Untitled 1](https://user-images.githubusercontent.com/80799025/177294955-ae420c30-13b9-42d3-8136-c1ab215a26fe.png)


 오른쪽 터미널과 같이 실행중인 노드들의 리스트가 출력됨을 확인할 수 있다.

 이를 이용하면 실행한 프로그램의 노드의 이름을 유추할 수 있다.

 예를들어 아래와 같이 실행한 후, 다시 node list를 호출하면

```bash
$ run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r __ns:=/skidbot
```

![Untitled 2](https://user-images.githubusercontent.com/80799025/177295616-06cbb051-858f-4347-990a-5e78c524fda5.png)

사진과 같이 teleop_twist_keyboard라는 노드가 추가됨을 확인 할 수 있다.

node list는 실행중인 node의 리스트만 나열

만약 주고받는 데이터 형식뿐 아니라 특정 Node의 정보를 알고싶은 경우 `ros2 node info` 커맨드를 사용

```bash
$ ros2 node info /skidbot/skid_steer_drive_controller
```

 ![Untitled 3](https://user-images.githubusercontent.com/80799025/177295707-edf634e7-62ab-4196-b833-5b6a2e280e0d.png)

 더 자세한 정보들 (노드가 어떤 데이터를 주고받았는지) 알 수 있다.
  </br>
 </br>
 
## Rqt_Graph



 Node들 사이에 어떤 데이터들이 오가는지 그래프로 시각화

```bash
# rqt 패키지 설치
$ sudo apt install ros-foxy-rqt*
# 실행
$ rqt_graph
```

 처음에는 노드 1개를 제외하고 아무것도 나오지 않는다.  → 새로고침 눌러 그래프를 얻는다.

![Untitled 4](https://user-images.githubusercontent.com/80799025/177295757-dc2dbb58-d6ef-407c-acc8-181206fe12ac.png)

 다음과 같은 그래프를 얻었다.

 - 그래프의 동그라미 : Node
 - 화살표 : 데이터 이동 경로

 그래프를 참조하여 어느 부분이 잘못되었는지 확인하여 디버깅이 가능하다.
  </br>
 </br>
 
## Package



 아래 링크에 있는 폴더 하나하나가 폴더이다.

 [https://github.com/rnanosaur/nanosaur](https://github.com/rnanosaur/nanosaur)

![Untitled 5](https://user-images.githubusercontent.com/80799025/177295779-bf5f866d-b70c-4bf6-8bbf-d4dbd19f79fc.png)


 각각의 폴더가 하나의 패키지로, 각자 다른 역할을 수행한다.
  </br>
 </br>
 
**패키지를 나누는 이유**

 - 패키지를 나누지 않으면 코드 1줄 수정해도 전체를 빌드해야한다.
 </br>
 </br>
 
 **패키지에 대해**

 - 관련된 라이브러리, 모델링 파일들, 설정 파일들을 모아둔 폴더
 - 시뮬레이션, 하드웨어 관련, 모델링, 원격 조종 등으로 분리시킨 모듈패키지 만들기
 - `colcon build`가 수행되는 빌드의 단위
 </br>
  </br>
  
### 패키지 만들기



 ament를 이용하여 패키지를 만들 수 있다.

```bash
$ ros2 pkg create --build-type ament_cmake  <패키지이름> --dependencies rclcpp <종속성> 
$ ros2 pkg create --build-type ament_python <패키지이름> --dependencies rclpy <종속성> 
```

 cmake는 c++ 기반,  python은  python기반 패키지이다.

 예제로 패키지를 하나 만들어 보았다.

![Untitled 6](https://user-images.githubusercontent.com/80799025/177295809-07cd2c8e-aaa2-43e9-8a90-648f7c846e02.png)!

 test_pack이라는 패키지를 생성하였다.

 정상적으로 패키지가 생성됨을 확인였다.
