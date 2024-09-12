# exceptions.py

class MissingAttribute(Exception):
    def __init__(self, error: str):
        super().__init__(error)

class InvalidAttribute(Exception):
    def __init__(self, error: str):
        super().__init__(error)

class MissingModule(Exception):
    def __init__(self, module: str):
        super().__init__(f'You do not have the "{module}" module installed. Install it using "pip install {module}" and try again.')
