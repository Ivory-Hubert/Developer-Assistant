import os, sys
import time
import configparser
import platform
from pathlib import Path
from termcolor import colored
from rich.progress import track
from rich.console import Console
from rich.markdown import Markdown
import subprocess

from Modules.projects_manager import ProjectsManager
from Modules.config_manager import ConfigManager
from Modules.opener import Opener

class Interface:
    def __init__(self, color="light_blue"):
        self.version = "0.1.0"
        title = f"DA - {self.version}"

        if platform.system() == "Windows":
            os.system(f'title {title}')
        else:
            print(f'\33]0;{title}\a', end='', flush=True)
        
        self.projects_manager = ProjectsManager()

        self.config = ConfigManager('memory.ini')
        self.memory = self.config.load_memory()
        self.color = self.memory.get('color') or color
        
        #==Reusables==
        self.header = (colored(" Developer Assistant ", f"{self.color}"))
        self.clear_screen = 'cls' if platform.system() == 'Windows' else 'clear'
        self.user_path = os.environ.get('USERPROFILE') or os.environ.get('HOME', 'User')
        
        self.load()
    
    def load(self):
        #==Check for leftovers==
        ROOT = Path(__file__).resolve().parents[1]
        temp_log = ROOT / "Dev-Assistant" / "Projects" / "CHANGELOG.tmp"

        if os.path.exists(temp_log):
            while True:
                os.system(self.clear_screen)
                print(colored("Temporary changelog detected.\n", "yellow"))
                print(colored("D", "light_red") + "elete or " + colored("K", "light_red") + "eep?\n")
                choice = input(f"{self.user_path}> ").lower()
                if choice == "d":
                    os.remove(temp_log)
                    break
                elif choice == "k":
                    break
                else:
                    print(colored("\nPlease make a valid choice.", "light_red"))
                    time.sleep(1.5)

        #==Welcome message==
        os.system(self.clear_screen)
        message = (colored("Developer Assistant Ver. ", attrs=["bold"]) + (colored(self.version, f"{self.color}", attrs=["bold"])))
        status = (colored("Loading, please wait... ", attrs=["blink"]))
        
        print(message.center(85))
        print("")
        print(status.center(73))
        
        #==Progress bar==
        for i in track(range(20)):
            time.sleep(0.10)

        #==Check intro state==
        intro = self.memory.get('intro')
        if intro == "True":
            self.intro()
        
        self.menu()
        
    def menu(self):
        while True:
            os.system(self.clear_screen)
            print("Main menu")
            print(self.header.center(127, "="))
            print("\nE. Exit\n")
            print("1. Projects")
            print("2. Settings\n")

            choice = input(f"{self.user_path}> ").strip()

            if choice.lower() == "e":
                os.system(self.clear_screen)
                print(self.header.center(127, "="))
                print("Bye!")
                time.sleep(2)
                raise SystemExit

            elif choice == "1":
                self.projects()

            elif choice == "2":
                self.settings()
            else:
                print("")
                print(colored("Unknown option...", "light_red", attrs=["blink"]))
                time.sleep(2)
        
    def projects(self):
        config = ConfigManager('memory.ini')
        self.memory = config.load_memory()
        while True:
            os.system(self.clear_screen)
            print("Main menu / Projects")
            print(self.header.center(127, "="))
            print("E. Back\n")
            print(colored("1. The last project:", attrs=["underline"]))
            print(colored(self.memory.get('last_project'), f"{self.color}"))
            print("\n2. Start a new project.\n")
            print(colored("Continue a project.", attrs=["underline"]))
            print("Pinned:")
            print("a. " + colored(self.memory.get('pinned_project'), f"{self.color}"))
            print("b. " + colored(self.memory.get('pinned_project1'), f"{self.color}"))
            print("c. " + colored(self.memory.get('pinned_project2'), f"{self.color}"))

            print("")
            choice = input(f"{self.user_path}> ").strip()

            if choice.lower() == "e":
                return

            elif choice == "1":
                project = self.memory.get('last_project')
                if not project:
                    print(colored("\nLast project has not been defined...", "light_red", attrs=["blink"]))
                    time.sleep(2)
                else:
                    #==Call ProjectsManager==
                    self.projects_manager.load_project(f"{project}")

            elif choice == "2":
                #==Call ProjectsManager==
                self.projects_manager.new_project()

            elif choice.lower() in ("a", "b", "c"):
                #==If the pinned project is empty, return an error message==
                options_map = {
                    'a': 'pinned_project',
                    'b': 'pinned_project1',
                    'c': 'pinned_project2'
                }
                key = options_map.get(choice.lower())
                project_name = self.memory.get(key)
                if project_name == "":
                    print("")
                    print(colored(f"Project '{choice}' has not been defined...", "light_red", attrs=["blink"]))
                    time.sleep(2)
                else:
                    #==No error? Call ProjectsManager=
                    project = self.memory.get(key)
                    self.projects_manager.load_project(f"{project}")

            else:
                print("")
                print(colored("Unknown option...", "light_red", attrs=["blink"]))
                time.sleep(2)
    
    def settings(self):
        while True:
            os.system(self.clear_screen)
            print("Main menu / Settings")
            print(self.header.center(127, "="))
            print("E. Back\n")
            print(colored("Configuration options", attrs=["underline"]))
            print("1. Edit pinned projects [WIP]")
            print("2. Change program's color [WIP]\n")
            print(colored("Other options", attrs=["underline"]))
            print("3. Open memory.ini manually")
            print("4. Open the Projects folder\n")

            choice = input(f"{self.user_path}> ").strip()

            if choice.lower() == "e":
                return
            elif choice == "1":
                pass
            elif choice == "2":
                pass
            elif choice == "3":
                Opener.open("memory.ini")
            elif choice == "4":
                Opener.open("Projects")
            else:
                print("")
                print(colored("Unknown option...", "light_red", attrs=["blink"]))
                time.sleep(2)

    def intro(self):
        os.system(self.clear_screen)
        print(colored("Welcome to the Developer Assistant\n", f"{self.color}", attrs=["bold"]))
        print("Here's everything you need to get started:\n")

        time.sleep(2)

        ROOT = Path(__file__).resolve().parents[1]
        readme_file = ROOT / "Dev-Assistant" / "README.md"

        readme_content = ""
        with open(readme_file, "r", encoding="utf-8") as f:
            readme_content = f.read()

        MARKDOWN = readme_content
        console = Console()
        md = Markdown(MARKDOWN)
        console.print(md)

        input("\nContinue..." + colored("[Enter]", f"{self.color}"))

        self.config.update_memory("CONFIG", "intro", "False")

        self.menu()
            
if __name__ == "__main__":
    try:
        app = Interface()
    except KeyboardInterrupt:
        print("\n\n" + colored("Execution interrupted by the user. Exiting...", "magenta", attrs=["bold"]))
        time.sleep(2)
        try:
            sys.exit(0)
        except:
            os._exit(0)
