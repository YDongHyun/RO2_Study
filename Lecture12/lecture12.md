# ROS2_Service

## New Robot 예제

 먼저 패키지를 실행하여 예제를 실행한다.

```python
#패키지 빌드
$ cbp py_service_pkg
```

```bash
# Terminal 1
$ rosfoxy
$ ros2 launch gcamp_gazebo gcamp_world.launch.py

# Terminal 2
$ rosfoxy
# 새로운 로봇을 스폰
$ ros2 run py_service_pkg gazebo_model_spawner
```

새로운 로봇이 등장한 것을 볼 수 있다.

여기서 새로 등장한 로봇을 주행하기 위해서는 다음과 같이  명령어를 입력하여 주행 할 수 있다.

```bash
# terminal 1
$ rosfoxy
$ ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r __ns:=/skidbot2

# terminal 2
$ rosfoxy
$ ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r __ns:=/skidbot
```

![Untitled](https://user-images.githubusercontent.com/80799025/179168313-323a099d-4fd7-4bf2-ba5a-368edeb76149.png)

두개의 로봇을 각각 조종 할 수 있다.

이 예제를 통해서 Service에 개념에 대해 알아본다.

## ROS2 Service 개념

Client Node가 Server Node로 request를 주면, 해당 request에 대응하는 적절한 response가 다시 Client에게로 전달 된다.

Topic과 비슷해 보이만 둘의 차이가 있다.

- Topic은 여러 Node가 Subscirbe 가능한 반면, Service는 request가 온 대상에게만 reponse가능 (1대 1 통신)
- Service Server는 동시에 여러 request 처리 불가, 현재 작업이 끝나야 다음 request수행 가능
- Topic 지속적으로 publish를 하는 반면 Service는 1회성
- Topic은 불특정 node가 Subscribe의 대상이며, 지속적이고, Service는 요청하는 주체가 있으며, 빠르게 동작이 완료

두 차이점을 잘 익혀놓고 어떠한 경우에 사용할지 판단한다.

## ROS2 Service Commands

service를 다루는 기본 커맨드

다음 명령어를 입력하여 service list를 확인 할 수 있다.

```bash
$ ros2 service list
```

명령어를 실행한 결과가 너무 많아 찾기 힘들다.

이때  grep을 이용하여 검색이 가능하다.

```bash
$ ros2 service list | grep <service name>
```

## Service srv

Topic의 데이터 타입 : msg(message)

Service의 데이터 타입 : srv

```bash
#특정 service가 어떤 srv 타입을 쓰는지 검색
$ ros2 service type /spawn_entity
#특정 srv타입을 사용하는 service를 찾기
$ ros2 service find gazebo_msgs/srv/SpawnEntity
```

Topic과 마찬가지로 Service의 srv의 정보를 확인할 수 있다.

```bash
$ ros2 interface show gazebo_msgs/srv/SpawnEntity
```

![Untitled 1](https://user-images.githubusercontent.com/80799025/179168402-3ae1e547-2564-44fd-9a65-4a9eac167a09.png)

다음과 같이 정보가 나오는데, 여기서 - - - 라인의 의미를 살펴보아야 한다.

 ---는  request 와 response를 구분하는 선이다.

## Service Call Command

server에게 request 요청하는 것을 Call이라고 한다.

터미널을 커맨드로 Call하는 방법은 다음과 같다.

- `ros2 service call` `<service 이름>` `<srv 타입>` `'<srv 내용>'`

처음에 실행했던 예제에서 로봇을 삭제하기 위해 다음과 같이 수행했다.

```bash
#먼저 삭제하기 위한 service인 delete관련 service를 검색
$ ros2 service list | grep delete
/delete_entity

#검색된 service 조회
$ ros2 service type /delete_entity
gazebo_msgs/srv/DeleteEntity

#srv분석
$ ros2 interface show gazebo_msgs/srv/DeleteEntity
string name                       # Name of the Gazebo entity to be deleted. This can be either
                                  # a model or a light.
---
bool success                      # Return true if deletion is successful.
string status_message             # Comments if available.
```

grep을 이용한 검색을 통해 어떻게 로봇을 삭제해야 할지 유추할 수 있었다.

name 이라는 requset를 통해 모델을 지울수 있을것이다.

```bash
$ ros2 service call /delete_entity gazebo_msgs/srv/DeleteEntity "{name: 'skidbot'}"
```

![Untitled 2](https://user-images.githubusercontent.com/80799025/179168415-bb22bf00-b7fa-4ad8-8b9b-f51ee77f77ee.png)

다음과 같이 초록색 로봇이 사라진 것을 확인할 수 있다.

정상적으로 로봇을 삭제할 수 있었다.

## Entry Point

.py 파일로 Node를 구현하고 Build 하여도 ros2 run은 Entry Point를 설정하지 않으면 실행이 안될것이다.

EX)

```python
   entry_points={
        'console_scripts': [
            'cmd_vel_pub_node = py_topic_pkg.cmd_vel_pub:main',
            'endless_cmd_vel_pub_node = py_topic_pkg.endless_cmd_vel_pub:main',
            'laser_sub_node   = py_topic_pkg.laser_sub:main',
            'laser_raw_node   = py_topic_pkg.laser_raw:main',
            'parking_node     = py_topic_pkg.parking:main',
        ],
    },
)
```

다음과 같이 entry point를 설정하여 진입점을 만들어주어야 한다.

Entry Point의 문법은 다음과 같다.

`**<ros2 run 시 실행시킬 이름>**` = `**<패키지 이름>`. `<파일 이름>`**: `**<파일에서의 진입점 - 보통 main>**`

entry_points를 설정해준 후,  다시 빌드하면 노드를 정상적으로 실행할 수 있다.
