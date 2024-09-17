# XMLCord Documentation | Tags

### 1. Adding Tags

Tags in XMLCord allow you to customize bot behavior. They can be added in the `<config>` section of the bot's XML configuration. Example:

```xml
<config>
    <tag tag_name="tag_value"/>
</config>
```

### 2. Available Tags

Here are the available tags you can use in XMLCord:

- **case_insensitive**: Makes the command case insensitive, so you can use "!help", "!Help", "!hELp", etc.
   - **Value type**: Bool (true/false)
   - Example:
     ```xml
     <tag case_insensitive="true"/>
     ```
- **strip_after_prefix**: Allows you to add spaces between the prefix and the command, e.g.: "! help", "! ping", etc.
   - **Value type**: Bool (true/false)
   - Example:
     ```xml
     <tag strip_after_prefix="true"/>
     ```
- **ignore_self**: The bot ignores its own messages (e.g. in the 'on_message' event).
   - **Value type**: Bool (true/false)
   - Example:
     ```xml
     <tag ignore_self="true"/>
     ```
- **token**: Allows storing the bot token in a separate file (supported: `.env`, `.json`, `.yml` (YAML)), e.g., ".env".
   - **Value type**: String
   - Example:
     ```xml
     <tag token=".env"/>
     ```

### 3. Example Tag Definitions

Here are practical examples for common tag setups:

- **Basic Configuration**:

  ```xml
   <config>
      <tag case_insensitive="true"/>
      <tag strip_after_prefix="true"/>
      <tag ignore_self="true"/>
      <tag token=".env"/>
  </config>
  ```

### 4. Reporting Issues

If you encounter errors or unexpected behavior related to tags, please report them in the [Issues](https://github.com/MateOp1337/XMLCord/issues) tab on GitHub.

**Include details such as:**

- **Error Messages**: Any specific error messages received.
- **Tag Configuration**: The XML configuration of the tag causing the issue.
- **Steps to Reproduce**: How to reproduce the issue.
- **Additional Context**: Any additional information that may help diagnose the problem.

**Your feedback helps us improve XMLCord!**
