import subprocess
import sys

def install_package(package_name):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])

try:
    import requests
except ImportError:
    print('='*20)
    choice = input('It looks like you don\'t have the `requests` library installed. Would you like to install it? (Y/N): ')
    if choice.lower() == 'y':
        install_package('requests')
        print('Run script again.')
        exit()

def get_package_size(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    data = response.json()
    
    latest_version = data['info']['version']
    release_data = data['releases'][latest_version]
    
    total_size = sum(file['size'] for file in release_data)
    return total_size