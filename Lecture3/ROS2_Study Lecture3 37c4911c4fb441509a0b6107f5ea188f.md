# ROS2_Study Lecture3

# Windows10 ROS2



ROS2부터 Windows 10 지원
![Untitled](https://user-images.githubusercontent.com/80799025/177042447-a7a6d58b-d06e-4709-8b9b-a4c24bd816ca.png)


Windows 업데이트 확인으로 최신상태를 유지

## Install Dependencies



### Chocolatey

패키지 설치, 관리 프로그램

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

PowerShell 관리자 권한으로 실행(`windows` + `X` + `A`) 후 코드 입력하여 설치

![Untitled 1](https://user-images.githubusercontent.com/80799025/177042516-cb1922d6-db2e-4421-a61a-449b1ae33f85.png)


PowerShell 재시작 후, choco명령어를 입력하여 정상적으로 설치되었는지 확인

chocolatey를 통해 설치 가능한 패키지는 아래 링크에서 확인 가능

[Chocolatey Software | Packages](https://community.chocolatey.org/packages)

### Windows Terminal

리눅스의 Terminator랑 비슷한 도구

```powershell
choco install -y microsoft-windows-terminal
```

PowerShell에서 다음 명령어를 입력하여 설치

Window Terminal를 관리자 권한으로 실행

![Untitled 2](https://user-images.githubusercontent.com/80799025/177042539-6b8bae8c-028d-4c6a-8d4d-6b27e306b79d.png)

정상적으로 설치되었다.

<aside>
💡 다음과 같은 명령어로 화면을 분할할 수 있다.

- 화면 가로 분할 : `alt` + `shift` + `-`
- 자동 화면 분할 : `alt` + `shift` + `D`
- 화면간 이동 : `alt` + `화살표 키`
- 화면 종료 : `ctrl` + `shift` + `w`
</aside>

### Python

Terminal에 명령어를 입력

```jsx
choco install -y python --version 3.9.7
```

설치 후 Windows Terminal을 실행시켜 python을 입력하여 잘 설치되었는지 확인한다.

![Untitled 3](https://user-images.githubusercontent.com/80799025/177042553-b63195eb-1c78-4eb3-91ae-45057c46e55f.png)

정상적으로 설치되었다.

### Git

버전관리자인 Git을 설치

```powershell
> choco install git
> git version
```

![Untitled 4](https://user-images.githubusercontent.com/80799025/177042565-5b97d903-6a9c-4ee6-9f0d-297a7785de9e.png)

정상적으로 설치되었다.

### Visual C++ Redistributables

ROS 2 빌드를 위한  배포판  C++

```powershell
choco upgrade --checksum64 F3B7A76D84D23F91957AA18456A14B4E90609E4CE8194C5653384ED38DADA6F3 --checksum 99DCE3C841CC6028560830F7866C9CE2928C98CF3256892EF8E6CF755147B0D8 vcredist2010
choco install -y vcredist2010 vcredist2013 vcredist140
```

### Open SSL

여러 프로그램 설치 인증에 필요한 프로그램

공식홈페이지 이동 → Win64 OpenSSl 1.1.1p Msi 다운 및 설치

[Win32/Win64 OpenSSL Installer for Windows - Shining Light Productions (slproweb.com)](https://slproweb.com/products/Win32OpenSSL.html)

C:\Program Files\OpenSSL-Win64의 경로에 설치하였따.

설치 후 OpenSSL-win64의 위치를 확인한 후 다음 명령어를 입력

```powershell
> setx -m OPENSSL_CONF "C:\Program Files\OpenSSL-Win64\bin\openssl.cfg"
```

![Untitled 5](https://user-images.githubusercontent.com/80799025/177042605-e125b19a-4acf-47e7-94c1-1d5048e1e5a2.png)

시스템 환경변수에 OpenSSL 위치 추가

시스템 설정→ 시스템 → 고급시스템 설정 → 고급 (환경변수) → Path→ OpenSSL의 경로 입력

![Untitled 6](https://user-images.githubusercontent.com/80799025/177042608-c07e02ac-2697-459e-8da0-834591888674.png)

경로를 입력하여 환경변수에 추가하였다.

### Visual Studio 2019

통합개발환경

Community 버전 설치 

이미 설치되있는 프로그램이므로 설치과정은 생략하였다.

### CMake

운영체재에 상관없이 사용 가능ㅎ나 빌드 툴

```powershell
choco install -y cmake
```

설치 후, 환경변수에 cmake의 경로를 추가해준다

`C:\Program Files\CMake\bin`

### 추가 종속성 설치

Nuget이라는 것을 통해 외부 패키지를 추가 제거 가능

[Release 2020-02-24 · ros2/choco-packages (github.com)](https://github.com/ros2/choco-packages/releases/tag/2020-02-24)

링크에 들어가 log4xx0.10.0-2.nupkg를 제외하고 다운

C:\Users\Administrator\Downloads\depend 폴더에 모두 넣은 후 다음 명령어를 입력하여 설치한다.

```bash
> choco install -y -s C:\Users\Administrator\Downloads\depend asio cunit eigen tinyxml-usestl tinyxml2 log4cxx bullet
```

기타 파이썬 패키지 설치

```bash
> python -m pip install --upgrade pip
> python -m pip install -U catkin_pkg cryptography empy ifcfg lark-parser lxml netifaces numpy opencv-python pyparsing pyyaml setuptools rosdistro
> python -m pip install -U pydot PyQt5
```

### 마지막 종속성, Graphviz 설치

```jsx
> choco install graphviz
```

### OpenCV

OpenCV는 오픈소스 Computer Vision Library이다.

[https://github.com/ros2/ros2/releases/download/opencv-archives/opencv-3.4.6-vc16.VS2019.zip](https://github.com/ros2/ros2/releases/download/opencv-archives/opencv-3.4.6-vc16.VS2019.zip)

위 링크를 클릭하여 zip파일을 받은 후 C드라이브(`C:\opencv` )에 압축을 해제한다.

그 후 환경변수에  `C:\opencv\x64\vc16\bin` 위치를 추가한다.

![Untitled 7](https://user-images.githubusercontent.com/80799025/177042624-d792df7e-86fe-42ab-9a9f-1a27629bca80.png)

Windows Terminal을 통해 OpenCV전용 환경변수 추가 

```jsx
> setx -m OpenCV_DIR C:\opencv
```

## ROS2 설치



설치방법 2가지

- ~~Option 1 - releases version 설치~~
- Option 2 - aka.ms/ros 통한 빠른 설치

배포판을 설치할 경우 설치되는 패키지가 300개 정도 설치, aka.ms는 700여개 정도의 패키지를 설치

따라서 Option2를 통해 설치하였다.

windows terminal을 관리자 권한으로 실행시키고 다음 명령어 입력

```bash
> set ChocolateyInstall=c:\opt\chocolatey
> choco source add -n=ros-win -s="https://aka.ms/ros/public" --priority=1
> choco upgrade ros-foxy-desktop -y --execution-timeout=0
```

## 설치 후 개발환경 구축



- workspace 생성 후 colcon build 및 기본 커멘드 소개
- windows terminal 환경 Setup
- Gazebo 환경 Setup

### workspace 생성 후 colcon build

ROS2는 일반 cmd가 아닌 x64 Native Tools Command를 사용.

 x64 Native Tools Command를 관리자 권한으로 실행한 후 다음 명령어를 입력

```powershell
> c:\opt\ros\foxy\x64\setup.bat
> mkdir c:\gcamp_ros2_ws\src
> pushd c:\gcamp_ros2_ws

> cd src
> git clone https://github.com/Road-Balance/gcamp_ros2_basic.git
> cd ../
> colcon build --symlink-install --packages-select gcamp_gazebo

> c:\gcamp_ros2_ws>colcon build --symlink-install --packages-select gcamp_gazebo
```

![Untitled 8](https://user-images.githubusercontent.com/80799025/177042641-65cf0e51-fb54-438e-8ff4-09a4c1974836.png)

다음과 같은 성공메시지를 확인하였다.

터미널 종료 전 `**uuidgen**`를 입력하여 나오는 코드를 기억한다

(~~2de539fc-f5ac-4bde-bfeb-25eb1df728d6~~)

### Window terminal 환경 Setup

 x64 Native Tools Command를 실행하는것이 불편하기 때문에 Windows Terminal을 이용해 ROS2전용 Terminal를 제작

1.windows terminal을 연 후 설정  → Json파일 열기 클릭 → Visual Studio 자동 실행

`profiles` ⇒ `cmd.exe` 로 진입후 아래의 코드 입력\

```jsx
{
    "colorScheme": "One Half Dark",
    "commandline": "C:\\Windows\\System32\\cmd.exe /k \"C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\Common7\\Tools\\VsDevCmd.bat\" -arch=amd64 -host_arch=amd64 && set ChocolateyInstall=c:\\opt\\chocolatey&& c:\\opt\\ros\\foxy\\x64\\setup.bat&& c:\\gcamp_ros2_ws\\install\\setup.bat",
    "guid": "{**<your-uuid>**}",
    "hidden": false,
    "icon": "ms-appx:///ProfileIcons/{0caa0dad-35be-5f56-a8ff-afceeeaa6101}.png",
    "name": "ros2-foxy",
    "startingDirectory": "C:\\gcamp_ros2_ws"
}
```

<`your-uuid>`에 앞서구한 코드를 집어넣는다.

![제목_없음](https://user-images.githubusercontent.com/80799025/177042661-88f72030-6b9a-45e1-8bc4-c3ab5e457698.png)

다음과 같이 ros2-foxy가 새로 생긴것을 확인하였다.

### Gazebo 환경 Setup

ROS2의 시뮬레이션 프로그램

lecture2에서 리눅스에 설치하였던 프로그램과 동일한 프로그램

이미 Gazebo를 설치하였으므로 예제 모델을 실행

ros2-foxy에 아래 명령어를 입력

```jsx
setx -m HOME C:\gcamp_ros2_ws
setx -m HOMEPATH C:\gcamp_ros2_ws
setx -m GAZEBO_MASTER_URI http://localhost:11345
setx -m GAZEBO_MODEL_DATABASE_URI http://models.gazebosim.org
setx -m GAZEBO_RESOURCE_PATH C:\opt\ros\foxy\x64\share\gazebo-10
setx -m GAZEBO_PLUGIN_PATH C:\opt\ros\foxy\x64\share\gazebo-10\plugins
setx -m GAZEBO_MODEL_PATH C:\opt\ros\foxy\x64\share\gazebo-10\models
setx -m SDF_PATH C:\opt\ros\foxy\x64\share\sdformat\1.6
```

각 명령어를 실행할때 마다 **성공: 지정한 값을 저장했습니다.** 라는 문구가 나온다

예제 실행에 필요한 Package build작업 수행

```jsx
> pushd C:\gcamp_ros2_ws

> colcon build --symlink-install --packages-select custom_interfaces
> colcon build --symlink-install --packages-select py_service_pkg
> colcon build --symlink-install --packages-select gcamp_gazebo

> install\setup.bat
```

**데모 실행**

```bash
> ros2 launch gcamp_gazebo gcamp_world_windows.launch.py
```

![Untitled 9](https://user-images.githubusercontent.com/80799025/177042668-8acad099-635b-4d0c-a7ba-126f8b82df77.png)

다음과 같이 데모가 잘 실행됬음을 확인하였다.

Ctrl + C로 종료할 수 있다.
