## XMLCord Documentation | Commands

### 1. Creating Commands

To create a command, define it in the `<commands>` section of the bot's XML configuration. Example:

```xml
<commands>
  <my_command>
    <argument name='text' type='text'/>
    <message>
        <content>Command executed with argument: {argument(text)}</content>
    </message>
  </my_command>
</commands>
```

### 2. Available Command Attributes

Here are the attributes you can use for commands in XMLCord:

- **name**: The name of the command (e.g., `name='my_command'`).
- **description**: A description of the command's functionality (optional).
- **slash**: Set to `true` if the command should be available as a slash command (default is `true`). *New in version a1.0.5a*
- **prefix**: Set to `true` if the command should be available as a prefixed command (default is `true`). *New in version a1.0.5a*

### 3. Command Arguments

Specify and use arguments in commands as follows:

- **name**: The name of the argument (e.g., `name='text'`).
- **type**: The type of the argument (e.g., `text`, `number`).

**Argument Requirements:**

1. **Exact Names**: Argument names must match exactly with those defined in the command.
2. **Correct Types**: Use the appropriate data types (e.g., `text`, `number`).
3. **Valid Values**: Ensure values are valid and within expected ranges.

### 4. Command Handlers

Handle commands using the following:

- **Reply Messages**: Use the `<message>` tag within a command to specify the reply.
- **Logging**: Use the `<log>` tag to log information when a command is executed.

> **Note:** When using slash commands, ensure to use `<reply_message>` or `<reply_embed>`, otherwise you may encounter "interaction failed" errors.

### 5. Example Command Definitions

Here are practical examples for common command setups:

- **Echo Command**

```xml
<commands>
  <echo>
    <argument name='text' type='text'/>
    <message>
      <content>You said: {argument(text)}</content>
    </message>
  </echo>
</commands>
```

- **Add Numbers**

```xml
<commands>
  <add>
    <argument name='num1' type='number'/>
    <argument name='num2' type='number'/>
    <message>
      <content>Sum: {argument(num1) + argument(num2)}</content>
    </message>
  </add>
</commands>
```

### 6. Customizing Command Behavior

Customize command behavior with:

- **Dynamic Responses**: Use placeholders to customize responses based on command arguments.
- **Conditional Logic**: Implement conditional logic within command handlers based on arguments or command types.

### 7. Command Configurations

*New in version a1.0.5b*

Starting from version **a1.0.5b**, commands can be configured to respond as either slash, prefix, or both. This functionality is not yet available in version **a1.0.5a**. Here are a couple of examples:

```xml
<help slash='true' prefix='false'>
    <reply_embed>
        <title>Help embed</title>
        <description>Some text :P</description>
        <color>#ff0000</color>
    </reply_embed>
</help>
```

```xml
<help slash='false' prefix='true'>
    <reply_embed>
        <title>Help embed</title>
        <description>Some text :P</description>
        <color>#ff0000</color>
    </reply_embed>
</help>
```

### 8. Troubleshooting Commands

Common issues and resolutions:

- **Command Not Recognized**: Ensure the command is correctly specified in the XML and that the bot has the necessary permissions.
- **Invalid Argument Types**: Verify that argument types match the expected values in the XML.

### 9. Best Practices

Tips for effectively using commands:

- **Organize Commands**: Keep command definitions well-organized for easier management and debugging.
- **Optimize Performance**: Avoid overly complex logic in command handlers to maintain optimal performance.
- **Test Thoroughly**: Test commands in a development environment before deploying them.

### 10. Reporting Issues

If you encounter errors or unexpected behavior related to commands, please report them in the [Issues](https://github.com/MateOp1337/XMLCord/issues) tab on GitHub.

**Include details such as:**

- **Error Messages**: Any specific error messages received.
- **Command Configuration**: The XML configuration of the command causing the issue.
- **Steps to Reproduce**: How to reproduce the issue.
- **Additional Context**: Any additional information that may help diagnose the problem.

**Your feedback helps us improve XMLCord!**
