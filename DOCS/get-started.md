# XMLCord Docs | Get Started

## Requirements
Before running the project, make sure you have the following installed:

- **Python 3.8+**
- **discord.py 2.4+** (for creating Discord bots)
- Any additional dependencies listed in `requirements.txt`

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/MateOp1337/XMLCord.git
   cd XMLCord
   ```

2. **Install dependencies**:
   It's recommended to use a virtual environment to manage dependencies.

   MacOS/Linux:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   Windows:
   ```bash
   python -m venv venv
   source venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Configure your bot**:
   Update the XML configuration files with your bot's details, such as the token and command settings:
   - `bot.xml`: Contains the core configuration, commands, events, and other settings.
   - Make sure to update the token and other necessary fields.

5. **Run the bot**:
   After setting everything up, you can start the bot:
   ```bash
   python base.py
   ```

## Customizing Commands & Events

You can modify or add new commands by editing the `<commands>` section in the `bot.xml`. For events, such as `on_message` or `on_ready`, use the `<events>` section.

## Additional Notes

- Make sure to keep your bot token and sensitive data safe.
