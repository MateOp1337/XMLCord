# XMLBot Config Documentation

## 1. Overview

This document provides a comprehensive guide for configuring a bot using XML format. It covers bot settings, commands, events, tasks, and views.

## 2. Bot Configuration

The `<bot>` tag is the root element of your bot's XML configuration. It encapsulates all other configuration elements, including `<config>`, `<variables>`, `<commands>`, `<events>`, `<tasks>`, and `<views>`.

### Example

```xml
<bot>
    <config>
        <!-- Configuration settings here -->
    </config>
    <variables>
        <!-- Variables definitions here -->
    </variables>
    <commands>
        <!-- Command definitions here -->
    </commands>
    <events>
        <!-- Event definitions here -->
    </events>
    <tasks>
        <!-- Task definitions here -->
    </tasks>
    <views>
        <!-- View definitions here -->
    </views>
</bot>
```

### Elements within `<bot>`

- **`<config>`**: Contains general settings for the bot, including the bot's name, command prefix, and tag options.
- **`<variables>`**: Defines variables that can be used throughout the bot's configuration.
- **`<commands>`**: Specifies the commands the bot can execute, including their response messages and permissions.
- **`<events>`**: Handles different events that the bot can respond to, such as messages or user actions.
- **`<tasks>`**: Defines periodic tasks that the bot will execute at specified intervals.
- **`<views>`**: Creates interactive views with buttons and other UI elements for user interaction.

## 3. Configuration

The `<config>` tag contains general settings for the bot.

```xml
<config>
    <name>Your bot name</name>
    <prefix>-</prefix>
    <tag case_insensitive="true"/>
    <tag strip_after_prefix="true"/>
    <tag ignore_self="true"/>
    <tag token=".env"/>
</config>
```

- **`<name>`**: Name of the bot.
- **`<prefix>`**: Command prefix used to trigger bot commands.
- **`<tag>`**: Various tag options for handling command and message processing.
  - **`case_insensitive`**: Determines if the prefix should be case-insensitive.
  - **`strip_after_prefix`**: Strips the prefix from the command text.
  - **`ignore_self`**: If true, the bot ignores messages sent by itself.
  - **`token`**: Specifies the file where the bot token is stored.

## 4. Variables

Define and use variables within the bot configuration.

```xml
<variables>
    <my_variable>123</my_variable>
    <error_channel>1118200341641564332</error_channel>
</variables>
```

- **`<my_variable>`**: Example variable that can be used in the configuration.
- **`<error_channel>`**: Channel ID where error messages will be sent.

## 5. Commands

Define bot commands within the `<commands>` tag.

```xml
<commands>
    <help>
        <embed>
            <title>Help embed</title>
            <description>Some text :P</description>
            <color>#ff0000</color>
        </embed>
        <reply_message>
            <content>I like cheese!</content>
        </reply_message>
    </help>
    <!-- More commands here -->
</commands>
```

### Command Elements

- **`<embed>`**: Creates an embedded message with a title, description, and color.
- **`<reply_message>`**: Specifies the message to be sent in reply.

## 6. Events

Handle different events that occur in the bot.

```xml
<events>
    <on_ready>
        <log>Bot is ready!</log>
    </on_ready>
    <!-- More events here -->
</events>
```

### Event Elements

- **`<log>`**: Logs a message when the event is triggered.
- **`<channel_message>`**: Sends a message to a specified channel.

## 7. Tasks

Define periodic tasks to be executed by the bot.

```xml
<tasks>
    <my_task1 seconds="10" enabled="false">
        <channel_message id='{var(error_channel)}'>
            <content>Some text</content>
        </channel_message>
        <log>Sent message to error channel (my_task1)</log>
    </my_task1>
</tasks>
```

### Task Elements

- **`<seconds>`**: Interval at which the task should run.
- **`<enabled>`**: Whether the task is enabled or not.

## 8. Views

Create interactive views for user interaction.

```xml
<views>
    <my_view>
        <button>
            <label>Press me!</label>
            <style>blue</style>
            <on_click>
                <response type='message'>
                    <content>Hi!</content>
                    <ephemeral>true</ephemeral>
                </response>
            </on_click>
        </button>
        <!-- More buttons here -->
    </my_view>
</views>
```

### View Elements

- **`<button>`**: Defines a button within the view.
  - **`<label>`**: Button label.
  - **`<style>`**: Button style.
  - **`<on_click>`**: Action to be taken when the button is clicked.

## 9. Best Practices

- **Organize Configuration**: Keep your XML configuration well-structured and organized for ease of maintenance.
- **Test Changes**: Always test changes in a development environment before deploying them to production.
- **Document Changes**: Keep track of any changes made to the configuration for future reference.

## 10. Troubleshooting

- **Event or Command Not Working**: Check for correct XML structure and ensure all required permissions are set.
- **Error Messages**: Review error logs and verify variable values and channel IDs.

## 11. Reporting Issues

For any issues or bugs, please report them on the [GitHub Issues page](https://github.com/MateOp1337/XMLCord/issues).
