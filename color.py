
"""
Utility Class for printing colored text to the terminal.
"""
from enum import Enum

class Color(Enum):
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    def __str__(self):
        return self.value