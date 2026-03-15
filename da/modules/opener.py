from termcolor import colored
import subprocess
import platform
import os
import time

class Opener:
    @staticmethod
    def open(path):
        #==Check if path exists==
        if not os.path.exists(path):
            print(colored("\nThis path does not exist.", "light_red"))
            time.sleep(1)
            return
        #==Open if exists==
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

if __name__ == "__main__":
    Opener()
