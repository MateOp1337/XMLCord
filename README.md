# XMLCord

> ### Warning!
> XMLCord is currently in early Alpha stages and under active development. As such, it may contain bugs or exhibit instability.
> If you encounter redundant print statements, they are likely leftover from internal testing. You are free to remove them as needed.


**XMLCord** is a Discord bot framework that utilizes XML configuration for defining bot behaviors, commands, and events. This framework allows for dynamic command creation and event handling based on XML-defined specifications, providing an easy way to manage bot functionalities without hardcoding them directly into the code.

**Looking for documentation? Take a look here: [XMLCord documentation](/DOCS/HOME.MD).**

**[Get Started](/DOCS/get-started.md)**!

### Key Features

- **Dynamic Commands**: Define commands in XML, including their arguments and behaviors, and have them automatically registered with the bot.
- **Event Handling**: Specify event listeners and their associated actions in XML, allowing for complex event-driven interactions.
- **Configurable Arguments**: Support for various argument types, including strings, integers, lists, and dictionaries, with automatic type conversion.
- **Customizable Token Loading**: Flexible token retrieval from `.env`, `.yml`, or `.json` files based on XML configuration.
- **Error Handling**: Handles missing arguments and invalid data formats gracefully with descriptive error messages.
- **Package Management**: Automatically prompts for installation of required libraries if not present (e.g., `python-dotenv`, `pyyaml`).

### How It Works

1. **XML Configuration**: Define bot settings, commands, events, and variables in an XML file. The bot reads this XML to configure itself dynamically.
2. **Command Creation**: Commands are created based on XML definitions. Arguments are parsed and converted according to their specified types.
3. **Event Management**: Events are handled according to XML configurations, with actions like sending messages or executing scripts being performed as specified.
4. **Token Retrieval**: The bot retrieves its token from various sources as specified in the XML configuration, including environment files or configuration files.

### Getting Started

1. **Install Dependencies**: Ensure you have the necessary libraries installed. If not, the bot will prompt you to install them.
2. **Prepare XML Configuration**: Create and configure an XML file to define your bot’s settings, commands, and events.
3. **Run the Bot**: Execute the bot script to start the bot with the configurations specified in the XML.

### Example XML Configuration

```xml
<bot>
    <config>
        <name>Your bot name</name>
        <prefix>-</prefix>
        <token></token>
        <tag case_insensitive="true"/>
        <tag strip_after_prefix="true"/>
        <tag ignore_self="true"/>
        <tag token=".env"/>
    </config>
    <commands>
        <greet>
            <reply_message>
                <content>
                    Hi, {ctx.author.mention}!
                </content>
            </reply_message>
        </greet>
    </commands>
    <events></events>
</bot>
```

This example shows how to set up basic configurations, including the bot’s prefix, token source, and additional settings like case sensitivity and token file path.

### [Changelogs](CHANGELOG.md)

### Upcoming features
- More actions:
    - Manage channels
    - Manage users
    - Manage roles
    - Simple management of dictionaries, lists and some objects
    - Connection to external APIs
