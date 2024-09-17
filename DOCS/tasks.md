# XMLCord Documentation | Tasks

*New in version a1.0.2*

### Overview

Tasks in XMLCord are scheduled operations that execute at specified intervals. Each task can perform various actions such as sending messages, logging information, and more. Tasks are defined in the `<tasks>` section of the XML configuration.

### 1. Adding a Task

To add a task, define it within the `<tasks>` section. Here is an example of a task definition:

```xml
<tasks>
    <my_task1 seconds="10" enabled="false">
        <channel_message id='{var(my_channel_id)}'>
            <content>Some text</content>
        </channel_message>
        <log>Sent message to error channel (my_task1)</log>
    </my_task1>
</tasks>
```

### 2. Task Attributes

- **hours**: Specifies the interval in hours at which the task will be executed. 
  - **Value type**: Integer
  - **Example**: `hours="10"`

- **minutes**: Specifies the interval in minutes at which the task will be executed. 
  - **Value type**: Integer
  - **Example**: `minutes="10"`

- **seconds**: Specifies the interval in seconds at which the task will be executed. 
  - **Value type**: Integer
  - **Example**: `seconds="10"`

- **enabled**: Indicates whether the task is active or not.
  - **Value type**: Bool (true/false)
  - **Example**: `enabled="false"`

### 3. Task Elements

Within a task, you can define various elements to perform actions:

- **channel_message**: Sends a message to a specified channel.
  - **Attributes**: `id` (ID of the channel where the message will be sent)
  - **Example**:
    ```xml
    <channel_message id='{var(error_channel)}'>
        <content>Some text</content>
    </channel_message>
    ```

- **log**: Logs a message to the console.
  - **Example**:
    ```xml
    <log>Sent message to error channel (my_task1)</log>
    ```

### 4. Example Task Definitions

Here are some practical examples of task configurations:

#### Basic Task

Sends a message to a channel every 10 seconds:

```xml
<tasks>
    <basic_task seconds="10" enabled="true">
        <channel_message id='{var(error_channel)}'>
            <content>Task executed every 10 seconds</content>
        </channel_message>
    </basic_task>
</tasks>
```

#### Disabled Task

Defines a task that is currently disabled:

```xml
<tasks>
    <disabled_task seconds="30" enabled="false">
        <log>This task is currently disabled</log>
    </disabled_task>
</tasks>
```

### 5. Reporting Issues

If you encounter errors or unexpected behavior related to tasks, please report them in the [Issues](https://github.com/MateOp1337/XMLCord/issues) tab on GitHub.

**Include details such as:**

- **Error Messages**: Any specific error messages received.
- **Task Configuration**: The XML configuration of the task causing the issue.
- **Steps to Reproduce**: How to reproduce the issue.
- **Additional Context**: Any additional information that may help diagnose the problem.

**Your feedback helps us improve XMLCord!**
