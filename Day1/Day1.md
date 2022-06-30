# ROS2_Study  Day1

# ROS2란 무엇인가?

---

### 로봇을 어떻게 개발?

<aside>
💡

- 기구설계
- 임베디드
- 컴퓨터 비전 (카메라 데이터를 이용하여 작업)
- 웹 연동
- 시뮬레이션
- 머신러닝 등등
</aside>

## ROS의 등장

### ROS의 기능

---

- 기존에 존재하는 로봇 오픈소스 사용 가능
- 로봇 개발에 필요한 여러 툴 제공 (Debuging tool etc...)
- 동작에 있어 안전함을 보장하는 Robot OS

![Untitled](https://user-images.githubusercontent.com/80799025/176657482-b160c2bd-eb92-4317-bfcf-2a140b455b0a.png)

각 필요한 부분을 패키지로 만들어 하나의 로봇 서비스를 제작
ROS는 패키지라는 단위로 동작

<aside>
💡 ROS의 다양한 툴
-Simulation - Gazabo, Ignition, ISSAC, webots ->ROS를 위한 툴
-Embedded - rosserial (MCU, ECU와 communication), micro_ROS
-Visualization, Debug Tools - RViz, RQt  ->  시각화, 디버깅
</aside>

![Untitled 1](https://user-images.githubusercontent.com/80799025/176657501-5086739b-f238-4e11-81f7-e035c0d8871c.png)

Gazabo example

다음과 같은 프로그램으로 시뮬레이션

## ROS2 != ROS1

---

### 기존 ROS 단점

- RTOS사용 불가
- TCPROS 사용으로 실시간성 저해
- Python2 사용 등등

ROS가 실제 상용화에 부족하다 판단 따라서 ROS2를 개발.

### ROS2 등장
![Untitled 2](https://user-images.githubusercontent.com/80799025/176657511-e49b20b2-c70c-43e8-a287-0f8e110b0fe7.png)


- ROS1에 비해 더 많은 운영체제 지원,
- 사용자가 직접 터미널을 통해 master를 먼저 실행 -> 삭제
- DDS(실무에서 쓰이고 있는 방식) 통신방식 사용
- 성능 또한 비약적으로 발전
- 산업현장에서 매우 많이 사용됨

> 자율주행, 배달로봇, 산업용 로봇 등등 ROS의 사용범위는 광범위하다.
>
