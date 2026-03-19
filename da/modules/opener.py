import subprocess
import platform
import os
import time
from termcolor import colored

class Opener:
    @staticmethod
    def open(path):
        if not os.path.exists(path):
            print(colored("\nThis path does not exist.", "light_red"))
            time.sleep(1)
            return
        else:
            system = platform.system()
            if system == "Windows":
                subprocess.Popen(['explorer', path])
            elif system == "Darwin":
                subprocess.Popen(['open', path])
            else:
                subprocess.Popen(
                    ['xdg-open', path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            return
