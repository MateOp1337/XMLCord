# base.py

import discord
from discord.ext import commands, tasks
from discord.ui import View, Button, Select
from discord import SelectOption, ButtonStyle
import os
from typing import Callable, Dict, Any
from parser import parse
from XMLCord.exceptions import *

DEBUG_MODE = True

def clean_data(data: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(data, dict):
        if '#text' in data:
            return data['#text']
        return {k: clean_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_data(item) for item in data]
    return data

xml_data = parse('XMLCord/bot')

if DEBUG_MODE:
    print(f"Parsed XML Data: {xml_data}")

xml_bot = xml_data['bot']
config = clean_data(xml_bot.get('config', {}))
commands_list = clean_data(xml_bot.get('commands', {}))
events = clean_data(xml_bot.get('events', {}))
xml_tasks = clean_data(xml_bot.get('tasks', {}))
variables = clean_data(xml_bot.get('variables', {}))
views = clean_data(xml_bot.get('views', {}))

if DEBUG_MODE:
    print(20*'-')
    print(clean_data(xml_bot['views']))
    print(20*'-')

tags = {k: (v.lower() == 'true') if isinstance(v, str) and v.lower() in {'true', 'false'} else v for item in config.pop('tag', []) if isinstance(item, dict) for k, v in item.get('@attributes', {}).items()}
config['tags'] = tags

ignore_self = tags.get('ignore_self', False)

def get_token() -> str:
    token_from_config = config.get('token')
    if token_from_config:
        return token_from_config

    if 'token' in tags:
        token_tag = tags['token']

        if '.env' in token_tag:
            try:
                from dotenv import load_dotenv
            except ImportError:
                raise MissingModule('python-dotenv')
            else:
                load_dotenv()
                return os.getenv('TOKEN')

        elif '.yml' in token_tag:
            try:
                import yaml
            except ImportError:
                raise MissingModule('pyyaml')
            else:
                with open(token_tag, 'r') as file:
                    data = yaml.safe_load(file)
                    return data['token']

        elif '.json' in token_tag:
            import json
            with open(token_tag, 'r') as file:
                data = json.load(file)
                return data['token']

    raise ValueError("No valid token found")

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=config.get('prefix', '!'),
            intents=discord.Intents.all(),
            case_insensitive=tags.get('case_insensitive', False),
            help_command=None,
            strip_after_prefix=tags.get('strip_after_prefix', False)
        )

bot = Bot()

def create_dynamic_command(name: str, function: Callable):
    command = commands.Command(function, name=name)
    bot.add_command(command)

def hex_to_int(hex_str: str) -> int:
    hex_str = hex_str.lstrip('#')
    return int(hex_str, 16)

def convert_argument(value: str, arg_type: str):
    if arg_type in ['str', 'text', 'string']:
        return value
    elif arg_type in ['int', 'number', 'integer']:
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"Expected an integer, got '{value}'")
    elif arg_type in ['list', 'array']:
        return value.split()
    elif arg_type in ['dict', 'json']:
        try:
            import json
            return json.loads(value)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format: '{value}'")
    return value

def format_data(data: Any, vars: Dict[str, Any]) -> Any:
    if isinstance(data, dict):
        return {k: format_data(v, vars) for k, v in data.items()}
    elif isinstance(data, list):
        return [format_data(item, vars) for item in data]
    elif isinstance(data, str):
        return data.format(**vars)
    return data

def create_command_function(data: dict) -> Callable:
    async def func(ctx: commands.Context, *args):
        arguments = {}
        arg_list = data.get('argument', [])
        remaining_args = list(args)

        if isinstance(arg_list, dict):
            arg_list = [arg_list]

        for arg_def in arg_list:
            if isinstance(arg_def, dict) and '@attributes' in arg_def:
                attr = arg_def['@attributes']
                arg_name = attr['name']
                arg_type = attr.get('type', 'str')
                rest = attr.get('rest', 'false') == 'true'

                if rest:
                    arguments[arg_name] = ' '.join(remaining_args)
                    break
                else:
                    if not remaining_args:
                        raise ValueError(f"Missing argument: {arg_name}")
                    arg_value = remaining_args.pop(0)
                    arguments[arg_name] = convert_argument(arg_value, arg_type)
            else:
                raise ValueError("Invalid argument definition")

        if 'permissions' in data:
            permissions_data = data['permissions']
            permissions = []

            if isinstance(permissions_data, dict):
                for perm_name, perm_value in permissions_data.items():
                    if perm_name == '@attributes':
                        for perm, value in perm_value.items():
                            if value.lower() == 'true':
                                permissions.append(perm)
                    else:
                        permissions.append(perm_name)

            def check_permissions(perms, user):
                missing_permissions = [perm for perm in perms if not getattr(user.guild_permissions, perm, False)]
                if missing_permissions:
                    raise commands.MissingPermissions(missing_permissions)

            check_permissions(permissions, ctx.author)

        vars = {'ctx': ctx}
        vars.update({f'argument({k})': v for k, v in arguments.items()})
        vars.update({f'var({k})': v for k, v in variables.items()})

        for action_name, action_data in data.items():
            action_data = format_data(action_data, vars)

            if action_name == 'embed':
                if 'color' in action_data:
                    action_data['color'] = hex_to_int(action_data['color'])
                embed = discord.Embed(**action_data)
                await ctx.send(embed=embed)

            elif action_name == 'message':
                del action_data['@attributes']
                await ctx.send(**action_data, view=views_list[data.get('@attributes', {}).get('view')]())

            elif action_name == 'reply_message':
                view=views_list[action_data.get('@attributes', {}).get('view')]
                del action_data['@attributes']
                await ctx.reply(**action_data, view=view())

    return func

def create_event_function(data: dict, event: str) -> Callable:
    async def func(*args, **kwargs):
        if args and hasattr(args[0], 'author') and ignore_self and args[0].author.id == bot.user.id:
            return

        arguments = {}
        if 'argument' in data:
            arg_list = data.get('argument', [])
            if isinstance(arg_list, dict):
                arg_list = [arg_list]

            for i, arg_def in enumerate(arg_list):
                if isinstance(arg_def, dict) and '@attributes' in arg_def:
                    attr = arg_def['@attributes']
                    arg_name = attr['name']
                    arg_type = attr.get('type', 'str')

                    if i < len(args):
                        arg_value = args[i]
                        arguments[arg_name] = convert_argument(arg_value, arg_type)
                    else:
                        raise ValueError(f"Missing argument: {arg_name}")
                else:
                    raise ValueError("Invalid argument definition")

        vars = {f'argument({k})': v for k, v in arguments.items()}
        vars.update({f'var({k})': v for k, v in variables.items()})

        for action_name, action_data in data.items():
            action_data = format_data(action_data, vars)

            if action_name == 'log':
                print(action_data)
            elif action_name == 'run_script':
                exec(action_data)  
            elif action_name == 'channel_message':
                channel_id = int(action_data.get('@attributes', {}).get('id', '0').format(**vars))
                channel = await bot.fetch_channel(channel_id)
                if channel:
                    del action_data['@attributes']
                    await channel.send(**action_data)
            elif event == 'on_message':
                if action_name == 'embed':
                    if 'color' in action_data:
                        action_data['color'] = hex_to_int(action_data['color'])
                    embed = discord.Embed(**action_data)
                    await args[0].channel.send(embed=embed)
                elif action_name == 'reply_embed':
                    if 'color' in action_data:
                        action_data['color'] = hex_to_int(action_data['color'])
                    embed = discord.Embed(**action_data)
                    await args[0].reply(embed=embed)
                elif action_name == 'message':
                    await args[0].channel.send(**action_data)
                elif action_name == 'reply_message':
                    await args[0].reply(**action_data)

    return func

def create_dynamic_loop_function(data: dict) -> Callable:
    async def func():
        vars = ({f'var({k})': v for k, v in variables.items()})

        for action_name, action_data in data.items():
            action_data = format_data(action_data, vars)

            if action_name == 'log':
                print(action_data)
            elif action_name == 'run_script':
                exec(action_data)  
            elif action_name == 'channel_message':
                channel_id = int(action_data.get('@attributes', {}).get('id', '0').format(**vars))
                channel = await bot.fetch_channel(channel_id)
                if channel:
                    del action_data['@attributes']
                    await channel.send(**action_data)

    return func

def create_dynamic_loop(*, name: str, loop_func: Callable[..., Any], hours: float = 0, minutes: float = 0, seconds: float = 0, enabled: bool = False):
    hours = float(hours) if isinstance(hours, str) else hours
    minutes = float(minutes) if isinstance(minutes, str) else minutes
    seconds = float(seconds) if isinstance(seconds, str) else seconds

    @tasks.loop(hours=hours, minutes=minutes, seconds=seconds, name=name)
    async def dynamic_loop():
        await loop_func()
    
    return dynamic_loop

enabled_loops = []

def create_dynamic_button_function(data: dict):
    async def func(interaction: discord.Interaction):
        vars = ({f'var({k})': v for k, v in variables.items()})
        for action_name, action_data in data.items():
            action_data = format_data(action_data, vars)

            if action_name == 'log':
                print(action_data)
            elif action_name == 'run_script':
                exec(action_data)  
            elif action_name == 'channel_message':
                channel_id = int(action_data.get('@attributes', {}).get('id', '0').format(**vars))
                channel = await bot.fetch_channel(channel_id)
                if channel:
                    del action_data['@attributes']
                    await channel.send(**action_data)
            elif action_name == 'response':
                action_type = action_data['@attributes']['type']
                if action_type == 'message':
                    del action_data['@attributes']
                    await interaction.response.send_message(**action_data)
                elif action_type == 'defer':
                    await interaction.response.defer(
                        ephemeral=action_data.get('@attributes', {}).get('ephemeral'),
                        thinking=action_data.get('@attributes', {}).get('thinking')
                    )
                elif action_type == 'modal':
                    await interaction.response.send_modal(action_data['@attributes']['name'])
    
    return func

def create_dynamic_option_function(data: dict):
    async def func(interaction: discord.Interaction):
        vars = ({f'var({k})': v for k, v in variables.items()})
        for action_name, action_data in data.items():
            action_data = format_data(action_data, vars)

            if action_name == 'log':
                print(action_data)
            elif action_name == 'run_script':
                exec(action_data)  
            elif action_name == 'channel_message':
                channel_id = int(action_data.get('@attributes', {}).get('id', '0').format(**vars))
                channel = await bot.fetch_channel(channel_id)
                if channel:
                    del action_data['@attributes']
                    await channel.send(**action_data)
            elif action_name == 'response':
                action_type = action_data['@attributes']['type']
                if action_type == 'message':
                    del action_data['@attributes']
                    await interaction.response.send_message(**action_data)
                elif action_type == 'defer':
                    await interaction.response.defer(
                        ephemeral=action_data.get('@attributes', {}).get('ephemeral'),
                        thinking=action_data.get('@attributes', {}).get('thinking')
                    )
                elif action_type == 'modal':
                    await interaction.response.send_modal(action_data['@attributes']['name'])
    
    return func

def create_dynamic_buttons(data: dict) -> Callable:
    buttons = data['button']
    buttons_list = []
    
    colors_map = {
        'primary': ButtonStyle.primary,
        'blurple': ButtonStyle.primary,
        'blue': ButtonStyle.primary,
        'secondary': ButtonStyle.secondary,
        'gray': ButtonStyle.secondary,
        'grey': ButtonStyle.secondary,
        'success': ButtonStyle.success,
        'green': ButtonStyle.success,
        'danger': ButtonStyle.danger,
        'red': ButtonStyle.danger,
        'link': ButtonStyle.link
    }

    for button in buttons:
        class DynamicButton(Button):
            def __init__(self, btn_data):
                super().__init__(
                    style=colors_map[btn_data['style']],
                    label=btn_data['label'],
                    disabled=btn_data.get('@attributes', {}).get('disabled', False),
                    url=btn_data.get('url') if btn_data['style'] == ButtonStyle.link else None,
                    emoji=btn_data.get('emoji')
                )

            async def callback(self, interaction: discord.Interaction, btn_data=button):
                func = create_dynamic_button_function(btn_data['on_click'])
                await func(interaction)

        buttons_list.append(DynamicButton(button))

    return buttons_list

def create_dynamic_select_menus(data: dict) -> list:
    options = data['select_menu']['option']
    options_list = []

    class DynamicSelect(Select):
        def __init__(self, select_data):
            super().__init__(
                placeholder=select_data.get('@attributes', {}).get('placeholder', 'Choose an option...'),
                min_values=int(select_data.get('@attributes', {}).get('min_values', 1)),
                max_values=int(select_data.get('@attributes', {}).get('max_values', 1)),
                options=[
                    SelectOption(
                        label=opt['label'],
                        value=opt['@attributes']['value'],
                        description=opt.get('description'),
                        emoji=opt.get('emoji'),
                        default='default' in opt.get('@attributes', {})
                    )
                    for opt in options
                ]
            )

        async def callback(self, interaction: discord.Interaction):
            for option in options:
                if option['@attributes']['value'] in self.values:
                    func = create_dynamic_option_function(option['on_select'])
                    await func(interaction)

    options_list.append(DynamicSelect(data['select_menu']))

    return options_list

def create_dynamic_view(data: dict) -> Callable:
    buttons = create_dynamic_buttons(data)
    select_menus = create_dynamic_select_menus(data)
    
    class DynamicView(View):
        def __init__(self):
            super().__init__(timeout=None)

            for button in buttons:
                self.add_item(button)
            
            for select_menu in select_menus:
                self.add_item(select_menu)
    
    return DynamicView

for task_name, task in xml_tasks.items():
    attr = task['@attributes']
    func = create_dynamic_loop_function(task)
    
    dynamic_loop = create_dynamic_loop(
        name=task_name,
        loop_func=func,
        hours=attr.get('hours', 0),
        minutes=attr.get('minutes', 0),
        seconds=attr.get('seconds', 0),
        enabled=attr.get('enabled', False)
    )
    
    if attr.get('enabled', False) == True:
        enabled_loops.append(dynamic_loop)

for name, value in commands_list.items():
    print(f'Command found: {name}')
    
    func = create_command_function(value)
    create_dynamic_command(name, func)

for name, value in events.items():
    print(f'Event found: {name}')
    func = create_event_function(value, name)
    bot.add_listener(func, name)

views_list = {}
for name, value in views.items():
    print(f'View found: {name}')
    view = create_dynamic_view(value)
    views_list[name] = view

@bot.event
async def on_ready():
    for loop in enabled_loops:
        await loop.start()

TOKEN = get_token()
bot.run(TOKEN)
