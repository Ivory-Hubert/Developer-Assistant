import os, sys
import time
import platform
import subprocess
import shutil
from pathlib import Path

from termcolor import colored
from rich.progress import track
from rich.console import Console
from rich.markdown import Markdown

from da.modules.projects_manager import ProjectsManager
from da.modules.config_manager import ConfigManager
from da.modules.opener import Opener
from importlib import resources

class Interface:
    def __init__(self):
        self.version = "0.2.8"
        self.cls = 'cls' if platform.system() == 'Windows' else 'clear'

        title = f"DA - {self.version}"

        if platform.system() == "Windows":
            os.system(f'title {title}')
        else:
            print(f'\33]0;{title}\a', end='', flush=True)

        self.config = ConfigManager('memory.ini')

        self.memory = None
        self.color = None
        self.header = None
        self.user_path = None

        self.first_run = False
    
    def run(self):
        steps = [
            ("Initializing runtime...", self.runtime_init),
            ("Checking configuration...", self.config.data_check)
        ]

        for label, step in track(steps):
            os.system(self.cls)
            print(label.center(65))
            result = step()
            time.sleep(0.30)
            if isinstance(result, list):
                for msg in result:
                    print(msg.center(65))
                    time.sleep(2)

        temp_log = Path(__file__).parent / "CHANGELOG.tmp"

        if os.path.exists(temp_log):
            while True:
                os.system(self.cls)
                print(colored(f"Temporary changelog detected in:\n{temp_log}\n", "yellow"))
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
        
        state = "intro" if self.first_run else "menu"

        while state != "exit":
            if state == "intro":
                self.intro()
                state = "menu"

            elif state == "menu":
                result = self.menu()
                if result == "exit":
                    state = "exit"

    def menu(self):
        while True:
            os.system(self.cls)
            print("Main menu")
            print(self.header.center(127, "="))
            print("\nE. Exit\n")
            print("1. Projects")
            print("2. Settings\n")

            choice = input(f"{self.user_path}> ").strip()

            if choice.lower() == "e":
                os.system(self.cls)
                print(self.header.center(127, "="))
                print("Bye!")
                time.sleep(1)
                return "exit"

            elif choice == "1":
                self.projects()

            elif choice == "2":
                self.settings()
            else:
                print("")
                print(colored("Unknown option...", "light_red", attrs=["blink"]))
                time.sleep(1)
        
    def projects(self):
        projects_manager = ProjectsManager(
            config=self.config,
            color=self.color,
            header=self.header,
            cls=self.cls,
            user_path=self.user_path
        )
        while True:
            self.memory = self.config.load_memory()
            os.system(self.cls)
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
                    time.sleep(1)
                else:
                    projects_manager.load_project(f"{project}")

            elif choice == "2":
                projects_manager.new_project()

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
                    time.sleep(1)
                else:
                    project = self.memory.get(key)
                    projects_manager.load_project(f"{project}")

            else:
                print("")
                print(colored("Unknown option...", "light_red", attrs=["blink"]))
                time.sleep(1)
    
    def settings(self):
        while True:
            os.system(self.cls)
            print("Main menu / Settings")
            print(self.header.center(127, "="))
            print("E. Back\n")
            print(colored("Configuration options", attrs=["underline"]))
            print("1. Edit pinned projects [WIP]")
            print("2. Change program's color [WIP]\n")
            print(colored("Other options", attrs=["underline"]))
            print("3. Open memory.ini manually")
            print("4. Open the Projects folder")
            print("5. Open the Templates folder\n")

            choice = input(f"{self.user_path}> ").strip()

            if choice.lower() == "e":
                return
            #elif choice == "1":
                #pass
            #elif choice == "2":
                #pass
            elif choice == "3":
                Opener.open(self.config.memory_ini)
            elif choice == "4":
                Opener.open(self.config.projects_folder)
            elif choice == "5":
                Opener.open(self.config.templates_folder)
            else:
                print("")
                print(colored("Unknown option...", "light_red", attrs=["blink"]))
                time.sleep(1)

    def runtime_init(self):
        if not self.config.memory_ini.exists():
            self.local_init()
            self.first_run = True

        self.memory = self.config.load_memory()
        self.color = self.memory.get('color') or "light_blue"

        self.header = (colored(" Developer Assistant ", f"{self.color}"))
        self.user_path = os.environ.get('USERPROFILE') or os.environ.get('HOME', 'User')

    def local_init(self):
        default_files = resources.files("da.default")
        dest = self.config.memory_ini

        for item in default_files.iterdir():
            if item.name == "default-memory.ini":
                shutil.copy(item, dest)

        self.config.projects_folder.mkdir(parents=True, exist_ok=True)
        # Add Test-Project
        dest = self.config.projects_folder
        for item in default_files.iterdir():
            if item.name == "test-project.ini":
                shutil.copy(item, dest)

    def intro(self):
        os.system(self.cls)
        print(colored("Welcome to the Developer Assistant\n", f"{self.color}", attrs=["bold"]))
        print("Here's everything you need to get started...\n")

        time.sleep(2)

        readme_content = resources.files("da").joinpath("intro.md").read_text()

        MARKDOWN = readme_content
        console = Console()
        md = Markdown(MARKDOWN)
        console.print(md)

        input("\nContinue..." + colored("[Enter]", f"{self.color}"))

def main():
    try:
        app = Interface()
        app.run()
    except KeyboardInterrupt:
        print("\n\n" + colored("Execution interrupted. Exiting...", "cyan", attrs=["bold"]))
        time.sleep(1)
        sys.exit(0)

if __name__ == "__main__":
    main()
