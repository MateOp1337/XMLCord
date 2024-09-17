# XMLCord Documentation | Variables

*New in version a1.0.1*

### Overview

Variables in XMLCord allow you to store and use dynamic values throughout your bot’s configuration. Variables can be referenced in commands, messages, and other parts of the XML configuration. They are defined in the `<variables>` section of the XML file.

### 1. Adding Variables

To add a variable, define it within the `<variables>` section. Here is an example of a variable definition:

```xml
<variables>
    <my_variable>123</my_variable>
    <error_channel>12345678987654321</error_channel>
</variables>
```

### 2. Variable Elements

- **Variable Definition**: Each variable is defined by its name and value.
  - **Name**: The name of the variable.
  - **Value**: The value assigned to the variable. This can be a string, number, or any other supported data type.

  **Example**:
  ```xml
  <my_variable>123</my_variable>
  <error_channel>12345678987654321</error_channel>
  ```

### 3. Referencing Variables

Variables can be referenced throughout the XML configuration using the `{var(variable_name)}` syntax. 

**Example**:
```xml
<channel_message id='{var(error_channel)}'>
    <content>An error occurred!</content>
</channel_message>
```

### 4. Example Variable Definitions

#### Basic Variables

Defines variables for channel IDs and error messages:

```xml
<variables>
    <welcome_channel>123456789012345678</welcome_channel>
    <error_channel>12345678987654321</error_channel>
    <api_key>your_api_key_here</api_key>
</variables>
```

#### Referencing Variables in Commands

Uses variables within commands for dynamic content:

```xml
<commands>
    <greet>
        <reply_message>
            <content>Welcome to the server, {ctx.author.mention}! For support, please visit our support channel or website.</content>
        </reply_message>
    </greet>
</commands>
```

### 5. Reporting Issues

If you encounter issues or unexpected behavior related to variables, please report them in the [Issues](https://github.com/MateOp1337/XMLCord/issues) tab on GitHub.

**Include details such as:**

- **Error Messages**: Any specific error messages received.
- **Variable Configuration**: The XML configuration of the variables causing the issue.
- **Steps to Reproduce**: How to reproduce the issue.
- **Additional Context**: Any additional information that may help diagnose the problem.

**Your feedback helps us improve XMLCord!**
