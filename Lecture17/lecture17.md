# Action 프로그래밍 - C++

저번강의에서 본 예제를 C++로 작성한 코드를 살펴보았다.

## Action Server 작성

Action Server의 코드를 살펴보았다.

이번 예제도  Python과 같이 피보나치 예제이다.

```cpp
// Copyright 2018 Open Source Robotics Foundation, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <memory>
#include <thread>

#include "custom_interfaces/action/fibonacci.hpp"
#include "rclcpp/rclcpp.hpp"
// TODO(jacobperron): Remove this once it is included as part of 'rclcpp.hpp'
#include "rclcpp_action/rclcpp_action.hpp"

using Fibonacci = custom_interfaces::action::Fibonacci;
using GoalHandleFibonacci = rclcpp_action::ServerGoalHandle<Fibonacci>;

class FBActionServer : public rclcpp::Node {
private:
  rclcpp_action::Server<Fibonacci>::SharedPtr m_action_server;

public:
  FBActionServer() : Node("fb_action_server") {
    using namespace std::placeholders;
    // Create an action server with three callbacks
    //   'handle_goal' and 'handle_cancel' are called by the Executor
    //   (rclcpp::spin) 'execute' is called whenever 'handle_goal' returns by
    //   accepting a goal
    //    Calls to 'execute' are made in an available thread from a pool of
    //    four.
    m_action_server = rclcpp_action::create_server<Fibonacci>(
        this, "fibonacci",
        std::bind(&FBActionServer::handle_goal, this, _1, _2),
        std::bind(&FBActionServer::handle_cancel, this, _1),
        std::bind(&FBActionServer::handle_accepted, this, _1));

    RCLCPP_INFO(get_logger(),
                "FB Action Server Created Waiting for client... ");
  }

  rclcpp_action::GoalResponse
  handle_goal(const rclcpp_action::GoalUUID &uuid,
              std::shared_ptr<const Fibonacci::Goal> goal) {
    RCLCPP_INFO(get_logger(), "Got goal request with order %d", goal->order);

    (void)uuid;

    // fibonacci가 9000이상의 큰 수를 반환요청하면 REJECT
    if (goal->order > 9000) {
      return rclcpp_action::GoalResponse::REJECT;
    }
    return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
  }

  rclcpp_action::CancelResponse
	// Cancel Request에 대해 reponse를 담당
  handle_cancel(const std::shared_ptr<GoalHandleFibonacci> goal_handle) {
    RCLCPP_WARN(get_logger(), "Got request to cancel goal");
    (void)goal_handle;
    return rclcpp_action::CancelResponse::ACCEPT;
  }
	
	// 
  void handle_accepted(const std::shared_ptr<GoalHandleFibonacci> goal_handle) {
    // thread사용하지 않으면 blocking될 수 있다.
    using namespace std::placeholders;
    std::thread{std::bind(&FBActionServer::execute, this, _1), goal_handle}
        .detach();
  }

  void execute(const std::shared_ptr<GoalHandleFibonacci> goal_handle) {
    RCLCPP_INFO(get_logger(), "Executing goal");
    rclcpp::Rate loop_rate(2);  // 0.5 sec

    const auto goal = goal_handle->get_goal();
		// shared pointer로서 생성 (벡터 형식)
    auto feedback = std::make_shared<Fibonacci::Feedback>();
    auto result = std::make_shared<Fibonacci::Result>();
    auto &sequence = feedback->partial_sequence;
    sequence.push_back(0);
    sequence.push_back(1);

    for (int i = 1; (i < goal->order) && rclcpp::ok(); ++i) {
      // cancel을 탐지, 탐지되었다면 루프 탈출
      if (goal_handle->is_canceling()) {
        result->sequence = sequence;
				// goal의 상태를 canceled
        goal_handle->canceled(result);
        RCLCPP_WARN(get_logger(), "Goal Canceled");
        return;
      }
      // Update sequence
      sequence.push_back(sequence[i] + sequence[i - 1]);
      // Publish feedback
      goal_handle->publish_feedback(feedback);
      RCLCPP_INFO(get_logger(), "Publish Feedback");

      loop_rate.sleep();
    }
    // Check if goal is done
    if (rclcpp::ok()) {
      result->sequence = sequence;
      goal_handle->succeed(result);
      RCLCPP_INFO(get_logger(), "Goal Succeeded");
    }
  }
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);

  auto server_node = std::make_shared<FBActionServer>();
  rclcpp::spin(server_node);

  rclcpp::shutdown();
  return 0;
}
```

## Action Client생성

이번에는  Client생성 코드를 살펴보았다.

```cpp
	FBActionClient() : Node("fb_action_client"), goal_handle(nullptr)
  {
		// 클라이언트 생성 매개변수 2개 (this, server이름)
    **m_action_client = rclcpp_action::create_client<Fibonacci>(this, "fibonacci");**
		// 0.5 초 후에 send_goal을 request
****    m_timer = create_wall_timer(std::chrono::milliseconds(500), std::bind(&FBActionClient::send_goal, this));

    RCLCPP_INFO(get_logger(), "FB Action Client Node Created");
  }
```

**send_goal**

```cpp
	void send_goal()
  {
    using namespace std::placeholders;

    // timer cancel required for send goal once
    m_timer->cancel();

		// request하는 server가 존재하는지 10초간 대기
    if (!m_action_client->wait_for_action_server(std::chrono::seconds(10)))
    {
      RCLCPP_ERROR(get_logger(), "Action server not available after waiting");
      rclcpp::shutdown();
    }

		// Goal message 준비
    auto goal_msg = Fibonacci::Goal();
    goal_msg.order = 10;

    auto send_goal_options = rclcpp_action::Client<Fibonacci>::SendGoalOptions();

    // goal response callback, feedback callback, resutl callback을 모두 연동후 async_send_goalfh  goal_send 수행	
    send_goal_options.goal_response_callback = std::bind(&FBActionClient::goal_response_callback, this, _1);
    send_goal_options.feedback_callback = std::bind(&FBActionClient::feedback_callback, this, _1, _2);
    send_goal_options.result_callback = std::bind(&FBActionClient::result_callback, this, _1);
		// async_send_goal을 통해 requset
    m_action_client->async_send_goal(goal_msg, send_goal_options);
  }
```

callback은 총 3가지 콜백이 있다.

- goal_response_callback
- feedback_callback
- result_callback

 callback 함수를 하나씩 살펴보았다.

**goal_response_callback**

```cpp
// goal Requset에 대한 Responde future 	
void goal_response_callback(std::shared_future<GoalHandleFibonacci::SharedPtr> future)
  {
		// goal reponse의 결과에 따라 로그 출력
		//  True 이면 accepted, False이면 rejected
    goal_handle = future.get();

    if (!goal_handle)
      RCLCPP_ERROR(get_logger(), "Goal was rejected by server");
    else
      RCLCPP_INFO(get_logger(), "Goal accepted by server, waiting for result");
  }
```

**feedback_callback**

```cpp
	// feedback메세지가 올때byby마다 출력
	// 첫 매개변수는  goal_handle이지만, 사용하지 않고, feedback 메세지가 올때마다 출력
	void feedback_callback(GoalHandleFibonacci::SharedPtr, const std::shared_ptr<const Fibonacci::Feedback> feedback)
  {
    std::cout << "Next number in sequence received: ";
		// feedback은 Vector형식 이므로 for문으로 출력
    for (auto number : feedback->partial_sequence)
      std::cout << number << " ";

    std::cout << std::endl;
  }
```

**result_callback**

```cpp
// 	
void result_callback(const GoalHandleFibonacci::WrappedResult& result)
  {
// switch문을 사용하여 케이스를 나눔 ( Succeeded, Aborted, Canceled
    switch (result.code)
    {
      case rclcpp_action::ResultCode::SUCCEEDED:
        break;
      case rclcpp_action::ResultCode::ABORTED:
        RCLCPP_ERROR(get_logger(), "Goal aborted");
        rclcpp::shutdown();
        return;
      case rclcpp_action::ResultCode::CANCELED:
        rclcpp::shutdown();
        RCLCPP_ERROR(get_logger(), "Goal canceled");
        return;
      default:
        RCLCPP_ERROR(get_logger(), "Unknown result code");
        return;
    }

    std::cout << "Result received: ";
		// result인 sequence는 벡터이므로 for문으로 순회
    for (const auto number : result.result->sequence)
      std::cout << number << " ";

    std::cout << std::endl;
    rclcpp::shutdown();
  }
```

## main부

main부의 코드를 분석하였다.

```cpp
while (rclcpp::ok())
{
  rclcpp::spin_some(client_node);
	// goal_response 도착시, goal_handle을 받음
  if (!client_node->is_goal_handle_none())
  {
		// get_result_future를 통해 Result Response future를 받음
    auto result_future = client_node->get_result_future();
		// 3초안에 Result를 받지 못하면 Cancel
    auto wait_result = rclcpp::spin_until_future_complete(client_node, result_future, std::chrono::seconds(3));

    if (wait_result == rclcpp::executor::FutureReturnCode::TIMEOUT)
    {
      RCLCPP_INFO(client_node->get_logger(), "Canceling goal");
      // Cancel the goal since it is taking too long
			//  get_cancel_result_future를 통해 Cancel future를 받고, future의 결과에 따라 cancel 성공 여부 판단
      auto cancel_result_future = client_node->get_cancel_result_future();
      if (rclcpp::spin_until_future_complete(client_node, cancel_result_future) !=
          rclcpp::executor::FutureReturnCode::SUCCESS)
      {
        RCLCPP_ERROR(client_node->get_logger(), "failed to cancel goal");
        rclcpp::shutdown();
        return 1;
      }

      RCLCPP_INFO(client_node->get_logger(), "goal is being canceled");

      while (rclcpp::ok())
        rclcpp::spin_some(client_node);
    }
    else if (wait_result != rclcpp::executor::FutureReturnCode::SUCCESS)
    {
      RCLCPP_ERROR(client_node->get_logger(), "failed to get result");
      rclcpp::shutdown();
      return 1;
    }
  }
}
```
