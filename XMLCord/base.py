import discord
import os
from discord.ext import commands
from parser import parse
from importer import install_package, get_package_size
from typing import Callable

xml_data = parse('bot')
xml_bot = xml_data['bot']
config = xml_bot['config']

commands_list = xml_bot['commands']
events = xml_bot['events']

tags = {k: (v.lower() == 'true') if isinstance(v, str) and v.lower() in {'true', 'false'} else v for item in config.pop('tag', []) if isinstance(item, dict) for k, v in item.get('@attributes', {}).items()}
config['tags'] = tags

def get_token():
    if config.get('token') is not None:
        return config.get('token')
    elif 'token' in tags:
        token_tag = tags['token']
        if '.env' in token_tag:
            try:
                from dotenv import load_dotenv
            except ImportError:
                size = get_package_size('python-dotenv')
                print('='*20)
                choice = input(f'It looks like you don\'t have the `python-dotenv` library installed.\nWould you like to install it?\nSize: {size / (1024 * 1024):.2f} MB (Y/N): ')
                if choice.lower() == 'y':
                    install_package('python-dotenv')
                    print('Run script again.')
                    exit()
            else:
                load_dotenv()
                return os.getenv('TOKEN')
        if '.yml' in token_tag:
            try:
                import yaml
            except ImportError:
                size = get_package_size('pyyaml')
                print('='*20)
                choice = input(f'It looks like you don\'t have the `pyyaml` library installed.\nWould you like to install it?\nSize: {size / (1024 * 1024):.2f} MB (Y/N): ')
                if choice.lower() == 'y':
                    install_package('pyyaml')
                    print('Run script again.')
                    exit()
            else:
                with open(token_tag, 'r') as file:
                    data = yaml.safe_load(file)
                    return data['token']
        if '.json' in token_tag:
            import json
            with open(token_tag, 'r') as file:
                data = json.load(file)
                return data['token']

class Bot(commands.Bot):
    def __init__(self):
        # Użycie tagów w inicjalizacji bota
        super().__init__(
            command_prefix=config.get('prefix', '!'),
            intents=discord.Intents.all(),
            case_insensitive=tags.get('case_insensitive', True),
            help_command=None,
            strip_after_prefix=tags.get('strip_after_prefix', True)
        )

bot = Bot()

def create_dynamic_command(name: str, function: Callable):
    command = commands.Command(function, name=name)
    bot.add_command(command)

def hex_to_int(hex_str: str) -> int:
    hex_str = hex_str.lstrip('#')
    return int(hex_str, 16)

def create_command_function(data: dict):
    async def func(ctx: commands.Context):
        print(data)
        
        for action_name, action_data in data.items():
            print(data.items())
            if action_name == 'embed':
                if 'color' in action_data:
                    action_data['color'] = hex_to_int(action_data['color'])
                embed = discord.Embed(**action_data)
                await ctx.send(embed=embed)
            
            elif action_name == 'run_script':
                eval(action_data)
            
            elif action_name == 'reply_embed':
                if 'color' in action_data:
                    action_data['color'] = hex_to_int(action_data['color'])
                embed = discord.Embed(**action_data)
                await ctx.reply(embed=embed)
            
            elif action_name == 'message':
                await ctx.send(**action_data)
            
            elif action_name == 'reply_message':
                await ctx.reply(**action_data)
     
    return func


def create_event_function(data: dict, event: str):
    async def func(*args, **kwargs):
        for action_name, action_data in data.items():
            # Log to console
            if action_name == 'log':
                print(action_data)
            
            # Run Python script
            elif action_name == 'run_script':
                eval(action_data)
            
            # On message actions
            if event == 'on_message':
                # Send embed
                if action_name == 'embed':
                    if 'color' in action_data:
                        action_data['color'] = hex_to_int(action_data['color'])
                    embed = discord.Embed(**action_data)
                    await args[0].send(embed=embed)
                    
                # Reply with embed
                elif action_name == 'reply_embed':
                    if 'color' in action_data:
                        action_data['color'] = hex_to_int(action_data['color'])
                    embed = discord.Embed(**action_data)
                    await args[0].reply(embed=embed)
                
                # Send message
                elif action_name == 'message':
                    await args[0].send(*action_data)
                
                # Reply with message
                elif action_name == 'reply_message':
                    await args[0].reply(*action_data)

    return func


for command in commands_list:
    for name, value in commands_list.items():
        print(f'Command found: {name}')
        print(f'Command {name}: {value}')
        
        func = create_command_function(value)
        create_dynamic_command(name, func)

for event in events:
    for name, value in events.items():
        print(f'Event found: {name}')
        print(f'Event {name}: {value}')
        
        func = create_event_function(value, name)
        bot.add_listener(func, name)

TOKEN = get_token()
bot.run(TOKEN)