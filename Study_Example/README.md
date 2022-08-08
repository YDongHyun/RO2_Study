## HelloWorld 패키지 만들기

helloworld 예제를 직접 코딩하고 분석해보면서 공부를 하였습니다.

**오류**

- setup.py의 entrypoint를 잘못 설정하여 노드가 실행되지 않았다. 코드를 수정하여 해결
- Publisher의 이름과 Subscriber의 이름이 달라 상호간의 통신이 안되었었다. 코드를 수정하여 해결

### package not found 오류

패키지가 설치된 폴더 이동 후 아래 명령어 실행을 통해 해결하였습니다.

```
colcon build
source install/setup.bash
```

### 커스텀 메시지 패키지 오류

Cmake 설정 변경중, 빌드시 다음과 같은 오류가 발생하였습니다.

`Unknown CMake command "rosidl_generate_interfaces".`

Cmake에 넣어야 하는 코드의 위치 잘못되어 오류가 발생,

코드의 위치를 수정하여 오류르 해결하였습니다.

### 커스텀 메시지 사용 오류

커스텀 메시지를 만들고 사용하려 하였지만 오류가 발생하였습니다.

Python 기준으로  `package.xml`파일을 수정하여 해결하였습니다.

(아래 내용 추가)

```
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

Ros 포럼에 있는대로 하면 오류 발생하였습니다.

```xml
다음과 같이 변경하여 오류 해결
<삭제 <build_depend>rosidl_default_generators</build_depend> >
<buildtool_depend>rosidl_default_generators</buildtool_depend>
```

### 커스텀 메시지 이름 오류

커스텀 메시지 이름에 오류가 발생하였습니다.

커스텀 메시지의 이름의 첫 글자를 대문자로 수정하여 오류를 해결하였습니다.

커스텀 메시지 빌드 오류

아래와 같은 오류가 발생하였습니다.

```xml
File "/opt/ros/foxy/share/ament_cmake_core/cmake/core/package_xml_2_cmake.py", line 21, in <module>
from catkin_pkg.package import parse_package_string
ModuleNotFoundError: No module named 'catkin_pkg'
```

```xml
아래 명령어로 패키지를 설치하여 오류 해결
$ pip install catkin_pkg
```

No module named 'lark’ 오류 발생

`pip install lark`로 해결하였습니다.

많은 오류 수정 끝에 커스텀 데이터 세팅을 마쳤습니.
