# ROS2_Study Lecture4

# 실습을 위한 Gazebo Simulation

---

이전 두 강의를 통해 ubuntu와 windows에 개발환경을 구축하였다.

이번 실습은 ubuntu로 진행하였다

## 환경구성

---

### 프로젝트 Clone && Build

터미널을 실행 한 후 아래 명령어를 입력

```bash
$ mkdir -p ~/gcamp_ros2_ws/src
# 디렉토리 생성
$ cd gcamp_ros2_ws/src
$ git clone https://github.com/Road-Balance/gcamp_ros2_basic.git

$ cd ~/gcamp_ros2_ws/
# 프로젝트 패키지 빌드
~~$ cbp gcamp_gazebo~~
# alias에 오류가 발생해 직접 코드를 입력하였다.
$ colcon build --symlink-install --packages-select gcamp_gazebo
```

빌드가 성공하였다.

### Gazebo 설정파일에 사용모델 경로 추가

배경 및 모델을 외부에서 가져오 위해 폴더를 Gazebo에 알려줘야 한다.

```bash
$ gedit ~/.gazebo/gui.ini

#user name을 ydh로 설정
[model_paths]
filenames=/home/<ydh>/gcamp_ws/src/gcamp_ros_basic/GazeboFiles/models

ex) /home/swimming/gcamp_ros2_ws/src/gcamp_ros2_basic/gcamp_gazebo/GazeboFiles/models
```

![Untitled](ROS2_Study%20Lecture4%20dd426f7346f94e1488985dbad7fd0785/Untitled.png)

다음과 같은 창이 뜨는데 경로를 파일에 붙여넣고 Save.

❗pwd 명령어를 통해 현재 폴더의 위치를 알 수 있다.

### Launch

아래 명령어를 입력하여 실행할 수 있다.  (최초 실행시 상당한 시간이 걸린다) 

**Anaconda와 같은 가상환경을 사용하면 실행 X, 반드시 deactivate** 

```bash
$ cd ~/gcamp_ros2_ws/
$ ~~rosfoxy~~
$ source /opt/ros/foxy/setup.bash && source ~/gcamp_ros2_ws/install/local_setup.bash
$ ros2 launch gcamp_gazebo gcamp_world.launch.py
```

![Untitled](ROS2_Study%20Lecture4%20dd426f7346f94e1488985dbad7fd0785/Untitled%201.png)

다음과 같이 Rviz와 Gazebo가 실행되었다.

Rviz로 로봇의 시점을 확인할 수 있다.

Gazobo 사용법

- 마우스 왼쪽 클릭 및 드래그 → 화면 이동
- 마우스 휠 → 확대/축소
- 마우스 휠 클릭 및 드래그 → 화면 회전
- 종료 방법 - `killg`
    
    ![프레젠테이션1.png](ROS2_Study%20Lecture4%20dd426f7346f94e1488985dbad7fd0785/%ED%94%84%EB%A0%88%EC%A0%A0%ED%85%8C%EC%9D%B4%EC%85%981.png)
    
1. 시점 이동
2. 물체 클릭 후 물체 이동
3. 물체 클릭 후 물체 회전
4. 물체 생성 
5. 빛 (광원) 생성
6. 복사, 붙여넣기\
7. 클릭 후 평면 시점 변경

Gazebo는 3차원 좌표체계를 가지고 있다.

### TeleOperation 실습

원격 조종 실습 ROS에서 지원하는 키보드를 통한 Gazebo상의 원격조종

`sudo apt install ros-foxy-teleop-twist-keyboard` 로 패키지 설치

```bash
# 새 터미널에서
$ ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r __ns:=/skidbot

Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

For Holonomic mode (strafing), hold down the shift key:
---------------------------
   U    I    O
   J    K    L
   M    <    >

t : up (+z)
b : down (-z)

anything else : stop

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%

CTRL-C to quit
```

다음 명령어를 실행하면 키보드로 로봇을 조작할 수 있다.

![Untitled](ROS2_Study%20Lecture4%20dd426f7346f94e1488985dbad7fd0785/Untitled%202.png)

Anaconda와 같은 가상환경을 사용하면 실행 X, 반드시 deactivate

Gazebo 종료시 killg 명령어로 종료

Gazebo는 종료가 잘 안되는 문제가 있다. 따라서 killg 명령어로 Gazebo를 종료한다.

---

+ xacro 관련 오류가 발생시에는 

```jsx
sudo apt install ros-foxy-xacro
```

위 명령어로 설치해준다.