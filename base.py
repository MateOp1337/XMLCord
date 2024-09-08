import discord
from discord.ext import commands, tasks
import os
from typing import Callable, Dict, Any
from parser import parse
from importer import install_package, get_package_size

def clean_data(data: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(data, dict):
        if '#text' in data:
            return data['#text']
        return {k: clean_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_data(item) for item in data]
    return data

xml_data = parse('bot')
print(f"Parsed XML Data: {xml_data}")

xml_bot = xml_data['bot']
config = clean_data(xml_bot['config'])
commands_list = clean_data(xml_bot['commands'])
events = clean_data(xml_bot['events'])
xml_tasks = clean_data(xml_bot['tasks'])
variables = clean_data(xml_bot['variables'])

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

        elif '.yml' in token_tag:
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
                await ctx.send(**action_data)

            elif action_name == 'reply_message':
                await ctx.reply(**action_data)

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
    
    if attr.get('enabled', False):
        enabled_loops.append(dynamic_loop)

for name, value in commands_list.items():
    print(f'Command found: {name}')
    print(f'Command {name}: {value}')
    
    func = create_command_function(value)
    create_dynamic_command(name, func)

for name, value in events.items():
    print(f'Event found: {name}')
    print(f'Event {name}: {value}')
    
    func = create_event_function(value, name)
    bot.add_listener(func, name)

@bot.event
async def on_ready():
    for loop in enabled_loops:
        await loop.start()

TOKEN = get_token()
bot.run(TOKEN)
