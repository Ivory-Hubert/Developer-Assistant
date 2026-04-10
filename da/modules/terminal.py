import os
import platform
import shutil

from termcolor import colored

from da.modules.config_manager import ConfigManager

class Terminal:
    def __init__(self):
        self.clear = "cls" if platform.system() == "Windows" else "clear"

        self.version = "0.3.7"
        
        title = f"DA - {self.version}"

        if platform.system() == "Windows":
            os.system(f"title {title}")
        else:
            print(f"\033]0;{title}\a", end="", flush=True)
        
        self.yes_cursor = "\033[?25h"
        self.no_cursor = "\033[?25l"

        self.user_path = None
        self.color = None
        self.header = None

        
    def main(self):
        self.user_path = os.environ.get("USERPROFILE") or os.environ.get("HOME", "User")

        config = ConfigManager("memory.ini", profile="Default")
        self.memory = config.load_memory()
        self.color = self.memory.get("color") or "light_blue"

        brand = colored(" Developer Assistant ", f"{self.color}")
        text = " Developer Assistant "

        columns, _ = shutil.get_terminal_size()
        pad_size = (columns - len(text)) // 2
        bars = "=" * max(0, pad_size)

        self.header = f"{bars}{brand}{bars}"



terminal = Terminal()
