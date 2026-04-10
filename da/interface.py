import os, sys
import shutil
import time
from importlib import resources
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.progress import track
from termcolor import colored

from da.modules.config_manager import ConfigManager
from da.modules.opener import Opener
from da.modules.projects_manager import ProjectsManager
from da.modules.terminal import terminal

class Interface:
    def __init__(self):
        self.config = ConfigManager("memory.ini", profile="Default")
        
        self.memory = None
        self.first_run = False

        terminal.main()
        term = terminal
        
        self.color = term.color
        self.header = term.header
        self.clear = term.clear
        self.user_path = term.user_path
        self.yes_cursor = term.yes_cursor
        self.no_cursor = term.no_cursor
        

    def run(self):
        steps = [
            ("Initializing runtime...", self.runtime_init),
            ("Checking configuration...", self.config.data_check),
        ]

        for label, step in track(steps):
            os.system(self.clear)
            print(label.center(65))
            result = step()
            time.sleep(0.30)
            if isinstance(result, list):
                for msg in result:
                    print(msg.center(65))
                    time.sleep(1)

        temp_log = Path(__file__).parent / "CHANGELOG.tmp"

        if os.path.exists(temp_log):
            while True:
                os.system(self.clear)
                print(colored("Unsaved changes detected from your last session!\n", "yellow",))
                print(
                    colored("D", "light_red")
                    + "elete or "
                    + colored("K", "light_red")
                    + "eep?\n"
                )
                choice = input(f"{self.user_path}> ").lower()
                if choice == "d":
                    os.remove(temp_log)
                    break
                elif choice == "k":
                    break
                else:
                    print(colored("\nPlease make a valid choice.", "light_red"))
                    time.sleep(0.5)

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
        self.active_profile = self.memory.get("profile")
        last_project = self.memory.get("last_project")

        projects_manager = ProjectsManager(config=self.config)

        while True:
            print(self.no_cursor)
            os.system(self.clear)
            print(
                colored(
                f"{self.active_profile}", f"{self.color}")
                + " / Main menu"
            )
            print(self.header)
            print("Q. Exit\n")
            print("Last project:")
            print(colored(last_project, f"{self.color}"))
            print("\n1. Projects")
            print("2. Profiles")
            print("3. Settings\n")

            choice = input(f"{self.user_path}{self.yes_cursor}> ").strip()

            if choice.lower() == "q":
                print(self.no_cursor)
                print(colored("Bye!", f"{self.color}", attrs=["bold"]))
                
                time.sleep(0.5)
                return "exit"

            elif choice == "1":
                projects_manager.projects(self.active_profile)

            elif choice == "2":
                return "profiles"

            elif choice == "3":
                return "settings"
            else:
                print(self.no_cursor)
                print(colored("Unknown option...", "light_red", attrs=["bold"]))
                time.sleep(0.5)

                
    def settings(self):
        while True:
            print(self.no_cursor)
            os.system(self.clear)
            print(
                colored(f"{self.active_profile}", f"{self.color}")
                + " / Main menu / Settings"
            )
            print(self.header)
            print("Q. Back\n")

            print(colored("Configuration options", attrs=["underline"]))
            print("1. Edit pinned projects [WIP]")
            print("2. Change program's color [WIP]\n")

            print(colored("Other options", attrs=["underline"]))
            print("3. Open memory.ini manually")
            print("4. Open the Projects folder")
            print("5. Open the Templates folder\n")

            choice = input(f"{self.user_path}{self.yes_cursor}> ").strip()

            if choice.lower() == "q":
                return
            # elif choice == "1":
            # pass
            # elif choice == "2":
            # pass
            elif choice == "3":
                Opener.open(self.config.memory_ini)
            elif choice == "4":
                Opener.open(self.config.projects_folder)
            elif choice == "5":
                Opener.open(self.config.templates_folder)
            else:
                print(self.no_cursor)
                print(colored("Unknown option...", "light_red", attrs=["bold"]))
                time.sleep(0.5)

                
    def profiles(self):
        while True:
            print(self.no_cursor)
            os.system(self.clear)
            print(
                colored(f"{self.active_profile}", f"{self.color}")
                + " / Main menu / Profiles"
            )
            print(self.header)
            print("Q. Back\n")

            print("1. Switch profiles\n")

            print("2. Create a new profile")
            print("3. Delete a profile\n")

            choice = input(f"{self.user_path}{self.yes_cursor}> ").strip()

            if choice.lower() == "q":
                return
            elif choice == "1":
                self.switch_profile()
            elif choice == "2":
                self.new_profile()
            elif choice == "3":
                self.delete_profile()
            else:
                print(self.no_cursor)
                print(colored("Unknown option...", "light_red", attrs=["bold"]))
                time.sleep(0.5)

                
    def switch_profile(self):
        prof_dir = self.config.profile_dir
        contents = os.listdir(prof_dir)

        print(f"\n{self.no_cursor}Your profiles:")
        for item in contents:
            print(" -" + colored(f" {item}", f"{self.color}"))

        name = input(f"\n{self.yes_cursor}Profile name > ").strip()

        if name in contents:
            self.load_profile(name)
            return
        else:
            print(colored("\nInvalid name!", "yellow"))
            time.sleep(0.5)
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

        self.load_profile(name)
        return

    def delete_profile(self):
        prof_dir = self.config.profile_dir
        contents = os.listdir(prof_dir)

        print(f"\n{self.no_cursor}Your profiles:")
        for item in contents:
            print(" -" + colored(f" {item}", f"{self.color}"))

        name = input(f"\n{self.yes_cursor}Profile name > ").strip()
            
        if name in contents and name != "Default":
            profiles = self.config.profile_dir
            profile = profiles / name
            shutil.rmtree(profile)

            if name == self.active_profile:
                self.load_profile(name="Default")
            return
        else:
            print(colored("\nInvalid name!", "yellow"))
            time.sleep(0.5)
            os.system(self.clear)

    def load_profile(self, name):
        self.config.update_memory("CONFIG", "profile", name)

        self.memory = self.config.load_memory()

        profile = self.memory.get("profile")
        self.config = ConfigManager("memory.ini", profile=profile)

        self.memory = self.config.load_memory()
        self.active_profile = self.memory.get("profile")

        
    def runtime_init(self):
        if not self.config.memory_ini.exists():
            self.local_init()
            self.first_run = True

        self.memory = self.config.load_memory()
        active_profile = self.memory.get("profile") or "Default"

        self.config = ConfigManager("memory.ini", profile=active_profile)
        self.memory = self.config.load_memory()

        
    def local_init(self):
        # Works together with ConfigManager.data_check()
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
        print(
            colored("Welcome to the Developer Assistant\n",
            f"{self.color}", attrs=["bold"]
            )
        )
        print("Here's everything you need to get started...\n")

        time.sleep(2)

        readme_content = resources.files("da").joinpath("intro.md").read_text()

        console = Console()
        md = Markdown(readme_content)
        console.print(md)

        input("\nContinue..." + colored("[Enter]", f"{self.color}"))

        # [WIP code, implementation could change]

        # print(colored("\nChoose an accent colour.\n", attrs=["underline"]))
        # print("1. Default - " + colored("light blue", f"{self.color}"))
        #
        # print("\n2. " + colored("red", "red"))
        # print("3. " + colored("green", "green"))
        # print("4. " + colored("blue", "blue"))
        # print("5. " + colored("yellow", "yellow"))
        # print("6. " + colored("cyan", "cyan"))
        # print("7. " + colored("magenta", "magenta"))
        #
        # print("\n8. " + colored("light green", "light_green"))
        # print("9. " + colored("light yellow", "light_yellow"))
        # print("10. " + colored("light magenta", "light_magenta"))
        # print("11. " + colored("light cyan", "light_cyan"))
        #
        # choice = input("\nChoice > ").strip()
        #
        # key_map = {
        #     "1": "",
        #     "2": "red",
        # }

def main():
    try:
        app = Interface()
        app.run()

        print(app.yes_cursor)
        os.system(app.clear)
        
    except KeyboardInterrupt:
        print(app.no_cursor)
        
        print(
            "\n\n"
            + colored("Execution interrupted. Exiting...", "cyan", attrs=["bold"])
        )
        
        time.sleep(0.5)

        print(app.yes_cursor)
        os.system(app.clear)
        
        sys.exit(0)

if __name__ == "__main__":
    main()
