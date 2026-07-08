# ROS 2 통신

> [!TIP]
> ROS 2에서는 노드(Node)들이 서로 데이터를 주고받기 위해 여러 가지 통신 방식을 제공한다.<br>
> 가장 많이 사용하는 통신은 Topic, Service, Action이며 노드의 설정을 관리하는 Parameters도 함께 사용된다.<br>
> 각각의 목적이 다르므로 상황에 맞는 통신 방식을 선택하는 것이 중요하다.

---

# Topic

### 정의
> [!NOTE]
> Topic은 Publisher가 데이터를 발행(Publish)하면 Subscriber가 이를 구독(Subscribe)하는 비동기(Asynchronous) 통신 방식이다.<br>
> 데이터를 지속적으로 전송할 때 사용하며 송신자는 수신자의 존재를 알 필요가 없다.<br>

- 특징<br>

> - Publisher → Subscriber 구조
> - 비동기 통신 방식
> - 1:N 또는 N:N 통신 가능
> - 실시간으로 데이터를 지속적으로 전송
> - 센서 데이터처럼 계속 변하는 정보 전달에 적합

### 통신 구조

```text
              Topic (/scan)
Publisher ────────────────────▶ Subscriber A
      │
      ├───────────────────────▶ Subscriber B
      │
      └───────────────────────▶ Subscriber C
```

### 동작 과정

```text
Publisher
    │
    │ Publish()
    ▼
+-------------+
|    Topic    |
+-------------+
    │
 ┌──┴─────────┐
 ▼            ▼
Sub A      Sub B
```

### 터미널 예시

토픽 목록 확인

```bash
ros2 topic list
```

토픽 정보 확인

```bash
ros2 topic info /scan
```

토픽 타입 확인

```bash
ros2 topic type /scan
```

토픽 데이터 확인

```bash
ros2 topic echo /scan
```

토픽 발행

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
"{linear: {x: 1.0}, angular: {z: 0.0}}"
```

토픽 주기 확인

```bash
ros2 topic hz /camera/image
```

토픽 대역폭 확인

```bash
ros2 topic bw /camera/image
```

### 사용 예시

> LiDAR 데이터, 카메라 이미지, IMU 데이터, GPS 정보, 로봇 속도(cmd_vel), 센서 데이터 전송 등<br>
> 지속적으로 데이터를 보내야 하는 대부분의 상황에서 사용된다.

---

# Service

### 정의

> [!NOTE]
> Service는 Client가 요청(Request)을 보내고 Server가 응답(Response)을 반환하는 동기(Synchronous) 통신 방식이다.<br>
> 요청을 보낸 노드는 응답을 받을 때까지 기다리며 한 번 요청하고 결과를 받아야 하는 작업에 적합하다.<br>

- 특징<br>

> - Client ↔ Server 구조
> - Request / Response 방식
> - 동기 통신
> - 일회성 작업 수행
> - 반드시 결과를 받아야 하는 작업에 적합

### 통신 구조

```text
Client
   │
   │ Request
   ▼
Server
   │
   │ Process
   ▼
Client

 Response
```

### 동작 과정

```text
Client                 Server

   │ ---- Request -----> │
   │                     │
   │ <--- Response ----- │
```

### 터미널 예시

서비스 목록

```bash
ros2 service list
```

서비스 타입 확인

```bash
ros2 service type /add_two_ints
```

서비스 정보 확인

```bash
ros2 service info /add_two_ints
```

서비스 호출

```bash
ros2 service call /add_two_ints \
example_interfaces/srv/AddTwoInts \
"{a: 10, b: 20}"
```

### 사용 예시

> 지도 저장, 센서 초기화, 계산 요청, 설정 변경, 로봇 리셋 등<br>
> 한 번 요청하고 결과만 받으면 되는 작업에서 사용된다.

---

# Action

### 정의

> [!NOTE]
> Action은 수행 시간이 오래 걸리는 작업을 위한 비동기 통신 방식이다.<br>
> Goal을 보내면 진행 상황(Feedback)을 받을 수 있고 작업이 끝나면 Result를 받으며 필요하면 작업을 취소(Cancel)할 수도 있다.<br>

- 특징<br>

> - Client ↔ Action Server 구조
> - Goal / Feedback / Result
> - 비동기 통신
> - 진행 상황 확인 가능
> - 작업 취소 가능

### 통신 구조

```text
Client
   │
   │ Goal
   ▼
Action Server
   │
   ├──── Feedback ─────▶ Client
   │
   ├──── Feedback ─────▶ Client
   │
   └──── Result ───────▶ Client
```

### 동작 과정

```text
Goal
 │
 ▼
Processing
 │
 ├── Feedback
 │
 ├── Feedback
 │
 ▼
Result
```

### 터미널 예시

액션 목록

```bash
ros2 action list
```

액션 정보

```bash
ros2 action info /fibonacci
```

Goal 전송

```bash
ros2 action send_goal \
/fibonacci \
example_interfaces/action/Fibonacci \
"{order: 10}"
```

Feedback 확인

```bash
ros2 action send_goal \
--feedback \
/fibonacci \
example_interfaces/action/Fibonacci \
"{order: 10}"
```

### 사용 예시

> Navigation, 경로 계획, 매니퓰레이터 제어, 장시간 계산, 물체 운반 등<br>
> 몇 초에서 몇 분 이상 걸리는 작업에 적합하다.

---

# Parameters

### 정의

> [!NOTE]
> Parameter는 노드 내부에서 사용하는 설정(Configuration) 값이다.<br>
> 프로그램을 다시 실행하지 않아도 실행 중 값을 변경할 수 있으며 ROS 2에서는 환경 설정을 위해 매우 자주 사용된다.<br>

- 특징<br>

> - 노드마다 독립적으로 존재
> - Key-Value 형태
> - 실행 중 변경 가능
> - YAML 파일과 함께 많이 사용

### 구조

```text
Node
├── use_sim_time
├── max_speed
├── frame_id
└── wheel_radius
```

### YAML 예시

```yaml
robot:
  ros__parameters:
    max_speed: 2.0
    wheel_radius: 0.15
    use_sim_time: true
```

### 터미널 예시

파라미터 목록

```bash
ros2 param list
```

파라미터 조회

```bash
ros2 param get /turtlesim background_r
```

파라미터 변경

```bash
ros2 param set /turtlesim background_r 255
```

파라미터 저장

```bash
ros2 param dump /turtlesim
```

YAML 적용

```bash
ros2 param load /turtlesim params.yaml
```

### 사용 예시

> 최대 속도, 센서 설정, PID Gain, Frame 이름, use_sim_time 설정 등<br>
> 프로그램의 동작을 설정하는 값들을 관리할 때 사용된다.

---

# Topic vs Service vs Action vs Parameters 비교

| 항목 | Topic | Service | Action | Parameters |
|------|--------|----------|---------|------------|
| 목적 | 데이터 전송 | 요청/응답 | 장시간 작업 | 설정값 관리 |
| 방식 | Publish / Subscribe | Request / Response | Goal / Feedback / Result | Key - Value |
| 동기 여부 | 비동기 | 동기 | 비동기 | 해당 없음 |
| 진행 상황 확인 | X | X | O | X |
| 작업 취소 | X | X | O | X |
| 대표 사용 | 센서 데이터 | 계산 요청 | Navigation | 환경설정 |

---

# 언제 사용할까?

```text
센서 데이터를 계속 보내야 한다.
        │
        ▼
      Topic

──────────────────────────────

한 번 요청하고 결과만 받으면 된다.
        │
        ▼
      Service

──────────────────────────────

작업 시간이 오래 걸리고
진행 상황(Feedback)을 확인하거나
중간에 취소(Cancel)할 수도 있어야 한다.
        │
        ▼
      Action

──────────────────────────────

노드의 설정값을 변경해야 한다.
        │
        ▼
    Parameters
```

---

# 전체 통신 관계

```text
                   ROS 2

         ┌──────── Node A ────────┐
         │                        │
  Publish│                     Client
         ▼                        │
       Topic                   Service
         ▲                        │
Subscribe|                     Server
         │                        │
         └─────── Node B ─────────┘
               ▲
               │
          Parameters

────────────────────────────────────

          Action Client
                │
                ▼
         Action Server
        Feedback / Result
```

---

# 자주 사용하는 명령어

노드 목록

```bash
ros2 node list
```

노드 정보

```bash
ros2 node info /node_name
```

인터페이스 목록

```bash
ros2 interface list
```

메시지 정의 확인

```bash
ros2 interface show geometry_msgs/msg/Twist
```

패키지 목록

```bash
ros2 pkg list
```

실행 가능한 노드 확인

```bash
ros2 pkg executables turtlesim
```

---

# 시각화 및 디버깅 도구

## rqt_graph

> [!TIP]
> 현재 실행 중인 ROS 2 시스템에서 노드와 Topic의 연결 관계를 그래프로 보여주는 도구이다.<br>
> Topic이 제대로 연결되어 있는지 확인할 때 가장 많이 사용한다.

실행

```bash
rqt_graph
```

---

## rqt

> [!TIP]
> 다양한 ROS 2 플러그인을 실행할 수 있는 GUI 프로그램이다.<br>
> Topic, Service, Parameter 등을 그래픽 환경에서 쉽게 확인할 수 있다.

실행

```bash
rqt
```

---

## RViz2

> [!TIP]
> ROS 2에서 가장 많이 사용하는 시각화 프로그램이다.<br>
> LiDAR, Camera, TF, Robot Model, PointCloud 등을 실시간으로 확인할 수 있다.

실행

```bash
rviz2
```

---

## TF(Frame) 확인

트리 생성

```bash
ros2 run tf2_tools view_frames
```

TF 확인

```bash
ros2 run tf2_ros tf2_echo map base_link
```

---

## Topic 주기 확인

```bash
ros2 topic hz /scan
```

---

## Topic 대역폭 확인

```bash
ros2 topic bw /camera/image
```

---

## Topic 지연 시간 확인

```bash
ros2 topic delay /scan
```

---

## ros2 bag

> [!TIP]
> Topic 데이터를 기록하고 다시 재생할 수 있는 도구이다.<br>
> 센서 데이터 저장, 디버깅, SLAM 테스트, 알고리즘 검증 등에 자주 사용된다.

기록

```bash
ros2 bag record /scan /odom
```

모든 Topic 기록

```bash
ros2 bag record -a
```

재생

```bash
ros2 bag play <bag_directory>
```

정보 확인

```bash
ros2 bag info <bag_directory>
```

---