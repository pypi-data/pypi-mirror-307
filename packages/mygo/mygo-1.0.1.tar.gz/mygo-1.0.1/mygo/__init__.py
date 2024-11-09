from typing import Union


class Version:
    def __init__(self, version_name: str = None, version_code: int = None, life_cycle: str = 'release'):
        self.name = version_name
        self.format_name: tuple = None
        self.code = version_code
        self.life_cycle = life_cycle.lower()

    def format(self):
        if self.name and self.name.replace('.', '').isdigit():
            self.format_name = tuple(self.name.split('.'))

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Version {self.life_cycle}-{self.name} {self.code}>'

    def __eq__(self, other: Union[str, 'Version']):
        if isinstance(other, str):
            other = Version(other)
        if isinstance(other, Version):
            if self.code and other.code:
                return self.code == other.code
            else:
                return self.name == other.name
        else:
            raise TypeError(f'Cannot compare {type(other)} with {type(self)}')

    def __lt__(self, other: Union[str, 'Version']):
        if isinstance(other, str):
            other = Version(other)
            if self.code and other.code:
                return self.code < other.code
