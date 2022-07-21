# Action 프로그래밍 - Python

## Action Server 작성

Action Server를 non-cancel, cancel 두가지 버전을 살펴보았다.

**fibonacci_action_server.py**

```bash
#!/usr/bin/env/ python3

# Copyright 2019 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# https://docs.ros.org/en/foxy/Tutorials/Actions/Writing-a-Py-Action-Server-Client.html#id4

import time

from custom_interfaces.action import Fibonacci

import rclpy
# server를 만들기 위한 헤더
from rclpy.action import ActionServer, GoalResponse
from rclpy.node import Node

#class 선언
class FibonacciActionServer(Node):
		# 초기값
    def __init__(self):
		# action서버 생성
        super().__init__('fibonacci_action_server')
        self.action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
		# 각 상황에 대한 callback을 지정
		# Goal Response가 오면, 우선 goal_callback을 실행시킨 뒤 execute_callback으로 넘어감
            goal_callback=self.goal_callback,
        )

        self.get_logger().info('=== Fibonacci Action Server Started ====')
		
		# async는 비동기, goal_callback후 진입
    async def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
				# Feedback action
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        for i in range(1, goal_handle.request.order):

            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()
				# 피보나치 함수
            feedback_msg.partial_sequence.append(
                feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i - 1]
            )
				# feedback publish
            self.get_logger().info(f'Feedback: {feedback_msg.partial_sequence}')
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        goal_handle.succeed()
        self.get_logger().warn('==== Succeed ====')
				#result반환
        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        return result

		#Goal Request 가장 처음 진입하는 callback
    def goal_callback(self, goal_request):
        """Accept or reject a client request to begin an action."""
        # This server allows multiple goals in parallel
        self.get_logger().info('Received goal request')
				#이 부분에 logic을 추가여 ACCEPT를 REJECT로 한다면 예외처리 가능
        return GoalResponse.ACCEPT

def main(args=None):
    rclpy.init(args=args)

    fibonacci_action_server = FibonacciActionServer()
    rclpy.spin(fibonacci_action_server)

    fibonacci_action_server.destroy()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

코드서 Action의 주요 기능들을 살펴보면 다음과 같다.

- Goal Response ⇒  `goal_callback`
- 중간 결과를 Feedback ⇒ `publish_feedback`
- 최종 Result Response ⇒ `Fibonacci.Result()`
- Feedback을 보내면서 내부 로직 실행 ⇒ `execute_callback()`
</br>

**ActionServer 생성**

위 코드에서 ActionServer를 생성한 부분이 있는데,  ActionServer는 다음과 같이 생성할 수 있다.

```python
self._action_server = ActionServer(
    self, <action-type>, "<action-name>", 
    <execute_callback>,
    <goal_callback>)
```

</br>

ActionServer 작성 - cancel ver.

저번 강의에서 잠깐 나왔던 `**MultiThreadedExecutor**`와 **`CancelResponse`**을 통해 코드가 작성되었다.

2번째 버전인 Cancel ver에 대한 코드를 살펴보았다.

위 코드에 변화된 부분을 집중적으로 보았다.

```python
import time

from custom_interfaces.action import Fibonacci

import rclpy
# 헤더에 CancelResponse,ReentrantCallBackGroup, MultiThreadedExecutor이 추가되었다.
*from rclpy.action import ActionServer, **CancelResponse**, GoalResponse*
**from rclpy.callback_groups import ReentrantCallbackGroup**
**from rclpy.executors import MultiThreadedExecutor**
from rclpy.node import Node
```

```python
self.action_server = ActionServer(
        self,
        Fibonacci,
        "fibonacci",
			#ReentrantCallBackGroup은 callback이 제한없이 병렬로 실행되도록 허용
        callback_group=ReentrantCallbackGroup(),
        execute_callback=self.execute_callback,
        goal_callback=self.goal_callback,
        cancel_callback=self.cancel_callback,
    )

def cancel_callback(self, goal_handle):
    """Accept or reject a client request to cancel an action."""
    self.get_logger().info("Received cancel request")

		# Logic 이부분에 내용추가로 예외처리 가능

    return CancelResponse.ACCEPT
```

</br>

### MultiThreadedExecutor

생성한 Node를 실행하는 executor는 SingleThrededExecutor, MultiThrededExecutor 2가지 존재

 MultiThreadedExecutor는 spin실행시 사용할 Node와 함께 전달하면multithreading 한다.
 
</br>

## Action Client 작성

actionClient 또한 2가지 버전으로 작성되었다.

먼저 non-cancel버전의 코드를 살펴보았다.

```python
# !/usr/bin/env/ python3
#
# Copyright 2019 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from custom_interfaces.action import Fibonacci

import rclpy
# ActionClient생성을 위한 헤더
from rclpy.action import ActionClient
****from rclpy.node import Node

class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__("fibonacci_action_client")
				# client 생성, Server에서 지정한 action 이름과 일치
        self.action_client = ActionClient(self, Fibonacci, "fibonacci")
****        self.get_logger().info("=== Fibonacci Action Client Started ====")

    def send_goal(self, order):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

				# 10초간 server를 기다림, 만약 이름이 일치하지 않으면 error 출력
				if self.action_client.wait_for_server(10) is False:
            self.get_logger().error("Server Not exists")

				# send_goal은 goal send시점에서 feeback_callback이 묶여 send_goal이 완료되는 시점의 goal_response_callback으로 이동
				# goal request가 제대로 보내졌는지 확인
        self._send_goal_future = self.action_client.send_goal_async(
				# feedback_callback은 지속적으로 feedback출력
            goal_msg, feedback_callback=self.feedback_callback
        )

				# server가 존재한다면, Goal Request의 성공 판단
				# goal_response_callback은 get_result_async가 완료되는 시점에 get_result_callback으로 이동
        self._send_goal_future.add_done_callback(self.goal_response_callback)

		# feedback을 받아옴
		# feedback의 결과를 출력
    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        print(f"Received feedback: {feedback.partial_sequence}")

		# Goal Request에 대한 응답 시 실행될 callback
    def goal_response_callback(self, future):
        goal_handle = future.result()

				# Goal Type에 따라 성공유무 판단
        if not goal_handle.accepted:
            self.get_logger().info("Goal rejected")
            return

        self.get_logger().info("Goal accepted")
				
        self._get_result_future = goal_handle.get_result_async()
				# get_result_callback은 최종 실행되는 함수로 Result출력
        self._get_result_future.add_done_callback(self.get_result_callback)

		# Result callback은 future를 매개변수로 받음
    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().warn(f"Action Done !! Result: {result.sequence}")
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)

    fibonacci_action_client = FibonacciActionClient()
		
		# Client Node 생성 이후 직접 send_goal
		# Goal Request에 대한 future를 반환
    future = fibonacci_action_client.send_goal(5)

    rclpy.spin(fibonacci_action_client)

if __name__ == "__main__":
    main()
```

</br>

## Action Client작성 - Cancel ver.

Action Client Cancel이 가능한 코드를 살펴보았다.

위의 코드와 차이나는 부분을 중심으로 살펴보았다.

```python
    def goal_response_callback(self, future):
        self.goal_handle = future.result()

        if not self.goal_handle.accepted:
            self.get_logger().info("Goal rejected")
            return
        
        self.get_logger().info("Goal accepted")

        # 2초 뒤 실행될 timer_callback을 선언, 이 예제에는 2초뒤 정지되도록 하였다.
****        self.timer= self.create_timer(2.0, self.timer_callback)

    def timer_callback(self):
        self.get_logger().info("Canceling goal")
        # cancel을 request
        future = self.goal_handle.cancel_goal_async()
				
				# future에 cancel 시점에 이뤄질 callback을 지정
        future.add_done_callback(self.cancel_done)
				#timer 정지
        self.timer.cancel()

		#cancel이 잘 되었는지 판단
    def cancel_done(self, future):
        cancel_response = future.result()
				# cancel의 성공 여부를 판단하는 로직
        if len(cancel_response.goals_canceling) > 0:
            self.get_logger().info("Goal successfully canceled")
        else:
            self.get_logger().info("Goal failed to cancel")

        rclpy.shutdown()
```
