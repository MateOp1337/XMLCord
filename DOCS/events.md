# XMLCord Documentation | Events

### 1. Creating Events

To create an event, add it to the `<events>` section in the bot's XML configuration. Example:

```xml
<events>
  <on_message>
    <argument name='message'/>
    <message>
        <content>You said: {argument(message).content}</content>
    </message>
  </on_message>
</events>
```

### 2. Available Events

Here are the events you can use in XMLCord:

- **on_ready**: Triggered when the bot is ready and connected to Discord.
- **on_message**: Triggered when a message is sent in a channel the bot has access to.
- **on_member_join**: Triggered when a new member joins the server.
- **on_member_remove**: Triggered when a member leaves the server.
- **on_message_edit**: Triggered when a message is edited.
- **on_message_delete**: Triggered when a message is deleted.
- **on_reaction_add**: Triggered when a reaction is added to a message.
- **on_reaction_remove**: Triggered when a reaction is removed from a message.
- **on_guild_join**: Triggered when the bot joins a new server.
- **on_guild_remove**: Triggered when the bot leaves a server.
- Other events available in discord.py.

**Note:** XMLCord may have issues handling certain events. [Learn more](#9-reporting-issues).

### 3. Event Arguments

Specify and use arguments in events as follows:

- **name**: The name of the argument (e.g., `name='message'`).
- **type**: The type of the argument (e.g., `text`, `number`).

**Argument Requirements:**

1. **Exact Names**: Argument names must match exactly with those in the [Discord.py documentation](https://discordpy.readthedocs.io/en/stable/).
2. **Correct Types**: Use the appropriate data types (e.g., `text`, `number`).
3. **Valid Values**: Ensure values are valid and within expected ranges.
4. **Documentation Consistency**: Cross-check with the latest Discord.py documentation for accuracy.

[Learn more about arguments](arguments.md)

### 4. Event Handlers

Handle different types of events using:

- **Reply Messages**: Use the `<message>` tag within an event to specify the reply.
- **Logging**: Use the `<log>` tag to log information when an event occurs.

### 5. Example Event Definitions

Here are practical examples for common event setups:

- **Greeting New Members**

```xml
<events>
  <on_member_join>
    <reply_message>
      <content>Welcome {ctx.author.mention} to the server!</content>
    </reply_message>
  </on_member_join>
</events>
```

- **Handling Edited Messages**

```xml
<events>
  <on_message_edit>
    <message>
      <content>Message edited: {argument(message).content}</content>
    </message>
  </on_message_edit>
</events>
```

### 6. Customizing Event Behavior

Customize event behavior with:

- **Dynamic Responses**: Use placeholders to customize responses based on event data.
- **Conditional Logic**: Implement conditional logic within event handlers based on arguments or event types.

### 7. Troubleshooting Events

Common issues and resolutions:

- **Event Not Triggering**: Ensure the event is correctly specified in the XML and that the bot has the necessary permissions.
- **Invalid Argument Types**: Verify that argument types match the expected values in the XML.

### 8. Best Practices

Tips for effectively using events:

- **Organize Events**: Keep event definitions well-organized for easier management and debugging.
- **Optimize Performance**: Avoid overly complex logic in event handlers to maintain optimal performance.
- **Test Thoroughly**: Test events in a development environment before deploying them.

### 9. Reporting Issues

If you encounter errors or unexpected behavior related to events, please report them in the [Issues](https://github.com/MateOp1337/XMLCord/issues) tab on GitHub.

**Include details such as:**

- **Error Messages**: Any specific error messages received.
- **Event Configuration**: The XML configuration of the event causing the issue.
- **Steps to Reproduce**: How to reproduce the issue.
- **Additional Context**: Any additional information that may help diagnose the problem.

**Your feedback helps us improve XMLCord!**
