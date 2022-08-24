ROS1의 noetic 버전을 설치하여 진행하였다.

## ROS1 패키지 빌드

ROS1의 패키지 빌드시 먼저 폴더를 생성해준다.

```xml
$ mkdir catkin_ws
$ cd catkin_ws
$ mkdir srv
```

Srv폴더로 이동한 후, 패키지를 생성한다.

```xml
$ catkin_create_pkg <package name> std_msgs rospy roscpp
```

package name뒤에 있는것은 종속성이다.

또한 ros1은 ros2와 달리 setup.bash파일의 위치가 install폴더가 아닌 devel폴더에 생성된다.

따라서 bashrc파일에 다음 source를 추가한다.

```xml
source ~/catkin_ws/devel/setup.bash
```

### ROS1 노드실행

노드를 실행하기 전, 생성된 노드파일을 `chmod +x <node>`를 해줘야한다.

ROS1의 노드를 실행하기 위해 먼저 새로운 터미널에 `roscore`를 실행한다.

빌드를 하기 위해서는 먼저 `catkin_ws`폴더로 이동해야한다.

그후 다음 명령어를 입력하면 build가 된다.

```xml
$ catkin_make
```

그후 새로운 터미널에 다음과 같은 명령어로 노드를 실행시킬 수 있다.

```xml
$ rosrun <package name> <node name.py>
```
