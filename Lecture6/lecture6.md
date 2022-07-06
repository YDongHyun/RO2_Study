# ROS2 Launch, lacuch file 작성

## launch file

.launch.py형식의 확장자

launch 명령어는 아래와 같다

`ros2 launch <패키지 이름> <launch 파일 이름>`

저번의 설치한 예제파일의 launch파일 경로

```bash
$ cd ~/gcamp_ros2_ws/src/gcamp_ros2_basic/gcamp_gazebo/launch
```

![Untitled](https://user-images.githubusercontent.com/80799025/177537484-4649b69c-7923-4ee7-88cc-be87dc8a505f.png)

다음과 같이 여러 런치파일을 확인할 수 있다.

- 예제중 하나를 열어보았다.
    
    ```python
    import os
    
    from ament_index_python.packages import get_package_share_directory
    from launch import LaunchDescription
    from launch.actions import ExecuteProcess, IncludeLaunchDescription
    from launch.launch_description_sources import PythonLaunchDescriptionSource
    from launch.substitutions import LaunchConfiguration
    
    from launch_ros.actions import Node
    
    # this is the function launch  system will look for
    def generate_launch_description():
        use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    
        rviz_file = "skidbot.rviz"
        robot_file = "skidbot.urdf"
        package_name = "gcamp_gazebo"
        world_file_name = "gcamp_world.world"
    
        # full  path to urdf and world file
        world = os.path.join(
            get_package_share_directory(package_name), "worlds", world_file_name
        )
        urdf = os.path.join(get_package_share_directory(package_name), "urdf", robot_file)
        rviz = os.path.join(get_package_share_directory(package_name), "rviz", rviz_file)
    
        # read urdf contents because to spawn an entity in
        # gazebo we need to provide entire urdf as string on  command line
        robot_desc = open(urdf, "r").read()
    
        # double quotes need to be with escape sequence
        xml = robot_desc.replace('"', '\\"')
    
        # this is argument format for spwan_entity service
        spwan_args = '{name: "skidbot", xml: "' + xml + '" }'
    
        robot_state_publisher_node = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}],
            arguments=[urdf],
        )
    
        # create and return launch description object
        return LaunchDescription(
            [
                # robot state publisher allows robot model spawn in RVIZ
                robot_state_publisher_node,
                # start gazebo, notice we are using libgazebo_ros_factory.so instead of libgazebo_ros_init.so
                # That is because only libgazebo_ros_factory.so contains the service call to /spawn_entity
                ExecuteProcess(
                    cmd=["gazebo", "--verbose", world, "-s", "libgazebo_ros_factory.so"],
                    output="screen",
                ),
                # tell gazebo to spwan your robot in the world by calling service
                ExecuteProcess(
                    cmd=[ "ros2", "service", "call", "/spawn_entity", "gazebo_msgs/SpawnEntity", spwan_args ],
                    output="screen",
                ),
                ExecuteProcess(
                    cmd=["ros2", "run", "rviz2", "rviz2", "-d", rviz], output="screen"
                ),
            ]
        )
    ```
    </br>
    
### .launch.py

Python문법을 기본적으로 사용

결과적으로 `**ExecuteProcess**`는 개별 커맨드로 실행 가능

위의 예제파일에서 중요한 아래부분을 확인

```python
  # create and return launch description object
    return LaunchDescription(
        [
            # robot state publisher allows robot model spawn in RVIZ
            robot_state_publisher_node,
            # start gazebo, notice we are using libgazebo_ros_factory.so instead of libgazebo_ros_init.so
            # That is because only libgazebo_ros_factory.so contains the service call to /spawn_entity
            ExecuteProcess(
                cmd=["gazebo", "--verbose", world, "-s", "libgazebo_ros_factory.so"],
                output="screen",
            ),
            # tell gazebo to spwan your robot in the world by calling service
            ExecuteProcess(
                cmd=[ "ros2", "service", "call", "/spawn_entity", "gazebo_msgs/SpawnEntity", spwan_args ],
                output="screen",
            ),
            ExecuteProcess(
                cmd=["ros2", "run", "rviz2", "rviz2", "-d", rviz], output="screen"
            ),
        ]
    )
```

ExecuteProcess가 3개가 반복됨을 볼 수 있다.

마지막 문단은 cmd=[  ] 형식으 되어있음을 확인했다.

아래 커맨드로 rviz를 실행해보았다.

```bash
$ rosfoxy
$ ros2 run rviz2 rviz2
```

실행 결과 rviz가 단독으로 실행됨을 확인하였다.

이를 통해 알 수 있는 사실은 예제의 launch file을 실행하면

gazebo 실행, robot 등장, rviz실행 3가지 작업이 동시에 동작한다는 것이다.
</br></br>


## ExecutProcess 방식

rviz만 동작시키는 launch file을 만들어 본다.

다음 명령어로 launch filed을 만든다

```python
$ cd ~/gcamp_ros2_ws/src/gcamp_ros2_basic/gcamp_gazebo/launch
$ touch first_launch.launch.py #새로운 파일을 만듬
$ gedit first_launch.launch.py #파일을 편집
```

파일에 예제 소스를 넣은 후 저장

이제 제작한 launch file을 빌드 후 실행한다.

```python
$ cd ~/gcamp_ros2_ws
$ cbp gcamp_gazebo
$ ros2 launch gcamp_gazebo first_launch.launch.py
```

실행 결과 rviz가 단독으로 실행됨을 확인하였다.
</br></br>

**문법**

- **`generate_launch_description`** :  ros2 launch 커멘드를 통해 launch file을 실행시키면, 이 이름을 가진 함수를 찾고 모든 launch file에는 빠지지 않고 제일 먼저 등장하는 함수
- `**LaunchDescription`** : 어떤 Node들을 실행시킬지 기술해둔 Description을 작성. 특정한 규칙으로 실행시킨 Node에 대한 옵션을 지정해주어야 하며, 여러 Node들의 실행이 필요할 수 있기에, 기본적으로 list의 구조를 가짐.
- `**ExecuteProcess`** : 프로세스 하나를 실행시킨다는 구분의 개념.
    - `**cmd`** :  터미널에서 입력하는 커멘드를 그대로 실행하고자 할 시에 사용.
    - `**output`** : Error log 등의 output이 출력되는 수단을 입력.
</br></br>

### Node 방식

각각의 노드 2개를 따로 실행하는것을  launch file 하나로 만들어 실행시는 예제

```bash
$ rosfoxy
$ ros2 run turtlesim turtlesim_node
$ ros2 run turtlesim draw_square
```

다음 명령어를 두 터미널에 실행하면 거북ㅋ이가 사각형을 그린다.

![Untitled 1](https://user-images.githubusercontent.com/80799025/177537518-bb017622-4993-49d8-942b-ff51323a4b5c.png)

이 명령을 수행하기 위해 2개의 터미널을 이용하였다.

그래서 노드방식을 이용해 두개의 작업이 동시에 실행되도록 launch file을 만들었다.

```jsx
$ cd ~/gcamp_ros2_ws/src/gcamp_ros2_basic/gcamp_gazebo/launch
$ touch second_launch.launch.py
$ gedit second_launch.launch.py
```

위 명령어로 launch file을 만든 후, 예제소스를 넣었다.

아래의 명령어로 launch file을 실행해보았다.

```jsx
$ cd ~/gcamp_ros2_ws
$ cbp gcamp_gazebo
$ ros2 launch gcamp_gazebo second_launch.launch.py
```

launch file 하나로 사각형을 그리는 거북이를 생성할 수 있었다.

- 방금 작성한 노드방식 launch file 코드이다.
    
    ```
    # this is the function launch  system will look for
    def generate_launch_description():
    
        turtlesim_node = Node(
            package='turtlesim',
            executable='turtlesim_node',
            parameters=[],
            arguments=[],
            output="screen",
        )
    
        turtlesim_teleop_node = Node(
            package='turtlesim',
            executable='draw_square',
            parameters=[],
            arguments=[],
            output="screen",
        )
    
        # create and return launch description object
        return LaunchDescription(
            [
                turtlesim_node,
                turtlesim_teleop_node,
            ]
        )
    ```
    

제일 아랫줄에서 보이듯이 노드방식을 사용하면 어떤것이 실행되는지 직관적으로 알 수 있다.
</br></br>

**문법**

- **`Node`** : Node 하나를 실행시킬  수 있는 옵션
    - `**package**` : 실행시킬 Node가 포함된 package를 선택
    - `**executable**` : c++ Node의 경우, colcon build를 하면 실행 가능한 프로그램 생성. python의 경우도 추가 작업이 필요.  기존 커멘드의 마지막 인자라고 생각.
    - `**parameters**` : 실행시킬 Node의 추가 매개변수
</br></br>

### parameter

yaml파일 형식  → parameter값을 적어놓은 파일

매개변수들을 하나의 파일로 정리한것이 parameter

[nanosaur_robot/camera.yml at 6aaf41d00c2f95d393d942d22e35c0a3c60fdf66 · rnanosaur/nanosaur_robot](https://github.com/rnanosaur/nanosaur_robot/blob/6aaf41d00c2f95d393d942d22e35c0a3c60fdf66/nanosaur_camera/param/camera.yml)

위 링크에서 보듯이 , yml(yaml) 파일 안에 parameter값들이 있음을 알 수 있다.

 parameter 파일을 사용하 위해 launch file py 파일 안에서 parameter파일을 가져와야 한다.
 </br></br>

### ExecuteProcss VS Node

Node방식이 더 직관적이므로 노드방식을 추천

두 방법을 혼용하여 상관없다.

<aside>
💡 오픈소스 패키지를 처음 사용하면 launch파일의 분석하여 많은것을 알 수 있다

</aside>
