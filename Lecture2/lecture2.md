
## 운영체제 설치

### 리눅스를 사용하는 이유

ROS2는 Window에서도 구동 가능하지만 대부분 마이크로프로세서는 리눅스 체제를 많이 쓰기 때문에 리눅스를 사용.

### 부팅 USB디스크를 이용하여 리눅스 설치

Linux Ubuntu 20.04를 데스크탑에 설치

grub을 설정하여 부팅시 윈도우와 리눅스 운영체제를 선택할 수 있도록 설정하였다

---

## 편의성 프로그램 설치

### Terminator

다중 분할 터미널을 위한 인터페이스.

```jsx
$ sudo apt update
# terminator 설치
$ sudo apt install terminator -y
```

sudo → 루트 권한(관리자 권한)

apt (Advanced Package Tool)은 우분투 패키의 관리자

터미널에 붙여넣을땐 Ctrl+Shift+v를 이용

**Terminator 단축어**

- `ctrl` + `shift` + `e` : 가로 분할
- `ctrl` + `shift` + `o` : 세로 분할
- `ctrl` + `shift` + `w` : 창 닫기
- `alt` + 화살표 : 창 간 이동

설치후 테스트 

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/3625a1bf-912d-4fab-b1d2-0436b169235a/Untitled.png)

정상적으로 terminator가 설치 실행이 됨을 확인했다.

### VScode : text editer

- 문법검사 가능
- 여러 Extension 지원
- 더욱 편리한 개발 작업 가능

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/dec55f2d-022d-4ea2-9edc-7229fad956c7/Untitled.png)

VScode 홈페이지 파일을 다운받은 후 터미널에서 압축을 풀어 설치

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/0b11304e-fdf9-4041-aa6d-130653d0db42/Untitled.png)

Screenshot from 2022-07-01 17-27-14VScode가 정상적으로 설치되었다.

### 추가설정

```jsx
$ sudo apt purge modemmanager

시리얼통신을 할때 방해되는 프로그램 삭제

$ sudo adduser [사용자 계정 이름]
$ sudo usermod -aG sudo [사용자 계정 이름]

사용자 계정 추가
```

---

## ROS2 Foxy 설치

```bash
$ locale  # check for UTF-8

$ sudo apt update && sudo apt install locales
$ sudo locale-gen en_US en_US.UTF-8
$ sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
$ export LANG=en_US.UTF-8

locale  # verify settings

$ sudo apt update && sudo apt install curl gnupg2 lsb-release -y
$ sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key  -o /usr/share/keyrings/ros-archive-keyring.gpg

$ sudo sh -c 'echo "deb [arch=$(dpkg --print-architecture)] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list'
$ sudo apt update

# Desktop Install (Recommended): ROS, RViz, demos, tutorials.
$ sudo apt install ros-foxy-desktop -y

# Install argcomplete (optional)
$ sudo apt install -y python3-pip
$ pip3 install -U argcomplete
```

터미널에 한줄씩 복사하여 설치

```bash
W: GPG error: http://packages.ros.org/ros2/ubuntu focal InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY F42ED6FBAB17C654
E: The repository 'http://packages.ros.org/ros2/ubuntu focal InRelease' is not signed.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.
```

다음과 같은 오류가 발생하여 아래 명령어를 입력하였다

```jsx
$ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F42ED6FBAB17C654
```

### Gazebo11 설치

- 로봇 시뮬레이션 프로그램
- ROS에서 공식으로 지원하는 프로그램

```bash
$ sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
$ wget https://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
$ sudo apt update

$ sudo apt install gazebo11 libgazebo11-dev -y

# Gazebo ROS 패키지들도 설치해줍니다.
$ sudo apt install ros-foxy-gazebo-ros-pkgs -y

# 설치 이후 실행을 통해 확인해 보세요!
$ gazebo
```

터미널에 복사하여 설치

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/9c4fcd56-0026-43f0-b9e4-863c69aad683/Untitled.png)

Gazebo가 정상적으로 설치되었다. 

Gazebo설치시 그림자가 보이지 않으면 그래픽 드라이버 설치

장치 확인

```bash
# 장착된 장치 확인
$ ubuntu-drivers devices
# 해당 장치에 맞는 드라이버 자동 설치
$ sudo ubuntu-drivers autoinstall
# 수동 설치
$ sudo apt install nvidia-driver-440 -y
# 설치 이후 재부팅
$ sudo reboot
```

자동으로 그래픽 드라이버를 설치하였다.

![Screenshot from 2022-07-01 18-08-40.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/33ee2345-8ac9-4bf7-b552-152ff501fe8a/Screenshot_from_2022-07-01_18-08-40.png)

정상적으로 그림자 출력 확인

### ROS 정상 설치 여부 확인

아래의 커맨드 라인을  2개의 터미널에 입력하여 ROS2가 잘 설치 되었는지 확인

```bash
# terminal 1
$ source /opt/ros/foxy/setup.bash
$ ros2 run demo_nodes_cpp talker
[INFO] [1615095938.051048376] [talker]: Publishing: 'Hello World: 1'
[INFO] [1615095939.051065032] [talker]: Publishing: 'Hello World: 2'
[INFO] [1615095940.051099193] [talker]: Publishing: 'Hello World: 3'
[INFO] [1615095941.051135001] [talker]: Publishing: 'Hello World: 4'
(...)

# terminal 2
$ source /opt/ros/foxy/setup.bash
$ ros2 run demo_nodes_py listener
[INFO] [1615095962.061778153] [listener]: I heard: [Hello World: 1]
[INFO] [1615095963.052502132] [listener]: I heard: [Hello World: 2]
[INFO] [1615095964.052535749] [listener]: I heard: [Hello World: 3]
[INFO] [1615095965.052742932] [listener]: I heard: [Hello World: 4]
(...)
```

두 터미널에서 같은 숫자가 출력되면 정상

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f0999710-2722-4bf4-9028-873609f1fb72/Untitled.png)

두 터미널에서 같은 숫자가 출력됨을 확인

따라서 ROS2와 Gazebo 설치가 완료되었다.

---

## 개발환경 설치

### Colcon Build system 설치

```jsx
$ sudo apt update
$ sudo apt install python3-colcon-common-extensions
```

위 명령어를 복사

### workspace 생성

ROS2는 종속성이 많음

소스코드 작업은 workspace라는 파일시스템에서 이루어져야 한다

```jsx
workspace 생성
$ source /opt/ros/foxy/setup.bash
$ mkdir -p ~/gcamp_ros2_ws/src
$ cd ~/gcamp_ros2_ws/src
```

git 명령어를 사용하기 위해 git을 설치

`$ sudo apt install git-all`

```jsx
$ git clone https://github.com/ros/ros_tutorials.git -b foxy-devel
$ ls ros_tutorials
> roscpp_tutorials  rospy_tutorials  ros_tutorials  turtlesim
```

workspace를 생성한 후 튜토리얼 패키지를 설치

```jsx
$ cd ../
$ rosdep install -i --from-path src --rosdistro foxy -y
> All required rosdeps installed successfully
```

특정 패키지가 필요하는 종속성을 자동으로 확인해주는 명령

```jsx
$ colcon build --symlink-install
$ ls
> build  install  log  src
```

colcon을 이용한 빌드

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/5446f90c-df36-46ef-8060-dd441fe84d15/Untitled.png)

최종적으로 빌드가 완료되었다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c58ff6fa-1151-449d-9f90-7cd9ba7c90e9/Untitled.png)

지정한 디렉토리 파일이 생성된것을 확인할 수 있다.

---

### Alias

- 길이가 긴 명령어를 단축어 설정
- ~/.bashrc를 수정하여 설정 `$ gedit ~/.bashrc`

```jsx
alias eb='gedit ~/.bashrc'
alias sb='source ~/.bashrc'

alias cba='colcon build --symlink-install'
alias cbp='colcon build --symlink-install --packages-select'
alias killg='killall -9 gzserver && killall -9 gzclient && killall -9 rosmaster'

**alias rosfoxy='source /opt/ros/foxy/setup.bash && source ~/gcamp_ros2_ws/install/local_setup.bash'**

source /usr/share/colcon_cd/function/colcon_cd.sh
export _colcon_cd_root=~/gcamp_ros2_ws
```

다음과 같이 Alias를 설정할 수 있다.

---

### turtlesim 실행

ROS의 상징과 같은 turtlesim을 실행하였다.

terminator를 이용하여 실행

```jsx
rosfoxy
ros2 run turtlesim turtlesim_node

# new terminal
rosfoxy
ros2 run turtlesim turtle_teleop_key
```

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/79a21591-269d-46ec-af9b-93348fdebb10/Untitled.png)

정상적으로 작동함을 확인하였다.

Ctrl+C 를 눌러 종료할 수 있다.
