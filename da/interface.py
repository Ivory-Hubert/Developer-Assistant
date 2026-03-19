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
        self.version = "0.3.5"
        self.clear = 'cls' if platform.system() == 'Windows' else 'clear'

        title = f"DA - {self.version}"

        if platform.system() == "Windows":
            os.system(f'title {title}')
        else:
            print(f'\33]0;{title}\a', end='', flush=True)

        self.config = ConfigManager('memory.ini', profile="Default")

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
            os.system(self.clear)
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
                os.system(self.clear)
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
                if result == "profiles":
                    self.profiles()
                    state = "menu"

                elif result == "settings":
                    self.settings()
                    state = "menu"

                elif result == "exit":
                    state = "exit"

    def menu(self):
        self.active_profile = self.memory.get('profile')

        projects_manager = ProjectsManager(
            config=self.config,
            color=self.color,
            header=self.header,
            cls=self.clear,
            user_path=self.user_path
        )

        last_project = self.memory.get('last_project')
        while True:
            os.system(self.clear)
            print(colored(f"{self.active_profile}", f"{self.color}") + " / Main menu")
            print(self.header)
            print("E. Exit\n")
            print("Last project:")
            print(colored(last_project, f"{self.color}"))
            print("\n1. Projects")
            print("2. Profiles")
            print("3. Settings\n")

            choice = input(f"{self.user_path}> ").strip()

            if choice.lower() == "e":
                os.system(self.clear)
                print(self.header)
                print("Bye!")
                time.sleep(1)
                return "exit"

            elif choice == "1":
                projects_manager.projects(self.active_profile)

            elif choice == "2":
                return "profiles"

            elif choice == "3":
                return "settings"
            else:
                print("")
                print(colored("Unknown option...", "light_red", attrs=["bold"]))
                time.sleep(1)
    
    def settings(self):
        while True:
            os.system(self.clear)
            print(colored(f"{self.active_profile}", f"{self.color}") + " / Main menu / Settings")
            print(self.header)
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
                print(colored("Unknown option...", "light_red", attrs=["bold"]))
                time.sleep(1)

    def profiles(self):
        while True:
            os.system(self.clear)
            print(colored(f"{self.active_profile}", f"{self.color}") + " / Main menu / Profiles")
            print(self.header)
            print("E. Back\n")

            print("1. Create a new profile")
            print("2. Switch profiles\n")

            choice = input(f"{self.user_path}> ").strip()

            if choice.lower() == "e":
                return
            elif choice == "1":
                self.new_profile()
            elif choice == "2":
                self.switch_profile()
            else:
                print("")
                print(colored("Unknown option...", "light_red", attrs=["bold"]))
                time.sleep(1)

    def switch_profile(self):
        while True:
            prof_dir = self.config.profile_dir
            contents = os.listdir(prof_dir)

            print("\nYour profiles:")
            for item in contents:
                print(colored(f" - {item}", f"{self.color}"))

            name = input("\nProfile name > ").strip()

            if name in contents:
                self.config.update_memory("CONFIG", "profile", name)

                self.memory = self.config.load_memory()

                profile = self.memory.get('profile')
                self.config = ConfigManager("memory.ini", profile=profile)

                self.memory = self.config.load_memory()
                self.active_profile = self.memory.get('profile')
                return
            else:
                print(colored("\nInvalid name!", "yellow"))
                time.sleep(1)
                os.system(self.clear)

    def new_profile(self):
        name = input("\nNew profile name > ").strip()

        profile_dir = self.config.profile_dir / name
        profile_dir.mkdir(parents=True, exist_ok=True)

        (profile_dir / "Projects").mkdir(exist_ok=True)
        (profile_dir / "Templates").mkdir(exist_ok=True)

        default_templates = resources.files("da.templates")
        for item in default_templates.iterdir():
            dest = profile_dir / "Templates"
            shutil.copy(item, dest)

        self.config.update_memory("CONFIG", "profile", name)

        self.memory = self.config.load_memory()

        profile = self.memory.get('profile')
        self.config = ConfigManager("memory.ini", profile=profile)

        self.memory = self.config.load_memory()
        self.active_profile = self.memory.get('profile')
        return

    def runtime_init(self):
        if not self.config.memory_ini.exists():
            self.local_init()
            self.first_run = True

        self.memory = self.config.load_memory()
        active_profile = self.memory.get("profile") or "Default"

        self.config = ConfigManager("memory.ini", profile=active_profile)
        self.memory = self.config.load_memory()

        self.color = self.memory.get('color') or "light_blue"
        self.user_path = os.environ.get('USERPROFILE') or os.environ.get('HOME', 'User')

        brand = (colored(" Developer Assistant ", f"{self.color}"))
        text = " Developer Assistant "

        columns, _ = shutil.get_terminal_size()
        pad_size = (columns - len(text)) // 2
        bars = "=" * max(0, pad_size)

        self.header = f"{bars}{brand}{bars}"

    def local_init(self):
        default_files = resources.files("da.default")
        dest = self.config.memory_ini

        for item in default_files.iterdir():
            if item.name == "default-memory.ini":
                shutil.copy(item, dest)

        self.config.projects_folder.mkdir(parents=True, exist_ok=True)

        dest = self.config.projects_folder
        for item in default_files.iterdir():
            if item.name == "test-project.ini":
                shutil.copy(item, dest)

    def intro(self):
        os.system(self.clear)
        print(colored("Welcome to the Developer Assistant\n", f"{self.color}", attrs=["bold"]))
        print("Here's everything you need to get started...\n")

        time.sleep(2)

        readme_content = resources.files("da").joinpath("intro.md").read_text()

        console = Console()
        md = Markdown(readme_content)
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
