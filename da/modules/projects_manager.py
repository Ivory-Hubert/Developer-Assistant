import os, sys
import time
import subprocess
import platform
from pathlib import Path

from termcolor import colored

from da.modules.config_manager import ConfigManager
from da.modules.version_logic import VersionLogic
from da.modules.opener import Opener

class ProjectsManager:
    def __init__(self, config, color, header, cls, user_path):
        self.config = config
        self.color = color
        self.header = header
        self.cls = cls
        self.user_path = user_path
    
    def projects(self, profile):
        self.active_profile = profile
        while True:
            self.memory = self.config.load_memory()
            os.system(self.cls)
            print(colored(f"{self.active_profile}", f"{self.color}") + " / Main menu / Projects")
            print(self.header.center(127, "="))
            print("E. Back\n")
            print(colored("1. Last project:", attrs=["underline"]))
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
                    self.load_project(f"{project}")

            elif choice == "2":
                self.new_project()

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
                    self.load_project(f"{project}")

            else:
                print("")
                print(colored("Unknown option...", "light_red", attrs=["blink"]))
                time.sleep(1)

    def new_project(self):
        os.system(self.cls)
        print(self.header.center(127, "="))
        print("E. Abort/back\n")
        
        name = input("Enter new project name: ")
        if name.lower() == "e":
            return
        path = input("\nEnter project path: ")

        changelog = input("\nProject changelog path: ")

        version = input("\nCurrent project version: ")

        cloud = input("\nCloud service (OneDrive/Azure/Dropbox/Google Drive): ")

        confirm = input("\nConfirm(Y) or abort(E): ")
        if confirm.lower() == "e":
            return
            
        elif confirm.lower() == "y":
            new_manager = ConfigManager(f"{name}.ini", profile=self.active_profile)
            new_manager.data = {
                "owner" : self.active_profile,
                "path": path,
                "changelog": changelog,
                "version": version,
                "cloud": cloud
            }
            new_manager.project_ini()
            return
            
        else:
            print("")
            print(colored("Unknown option, try again...", "light_red", attrs=["blink"]))
            time.sleep(2)
            return
            
    def load_project(self, project):
        version_logic = VersionLogic(
            config=self.config,
            color=self.color,
            header=self.header,
            cls=self.cls,
            user_path=self.user_path
        )

        load_manager = ConfigManager(f"{project}.ini", profile=self.active_profile)
        project_ini_path = load_manager.projects_folder / f"{project}.ini"

        while True:
            try:
                setting = load_manager.load_project()
            except KeyError:
                print(colored(f"\nCan't find {project}.ini", "light_red"))
                time.sleep(1)
                return

            os.system(self.cls)
            print(colored(f"{self.active_profile}", f"{self.color}") + " / Main menu / Projects / Project menu")
            print(self.header.center(127, "="))
            print("E. Back\n")
            print(colored("Chosen project:", attrs=["underline"]))
            print(colored(project, f"{self.color}"))
            print("\n1. Open project folder.")
            print("2. Manage the changelog.")
            print("3. Backup to the cloud. [WIP]")
            print("4. Open project configurations.")
            print("5. Restore backup changelog.\n")

            choice = input(f"{self.user_path}> ").strip()

            if choice.lower() == "e":
                return

            elif choice == "1":
                path = setting.get('path')
                folder = Path(path)
                Opener.open(folder)

            elif choice == "2":
                version_logic.project_menu(project, self.active_profile)

            #elif choice == "3":

            elif choice == "4":
                Opener.open(project_ini_path)

            elif choice == "5":
                changelog = Path(setting.get('changelog'))
                if os.path.exists(changelog):
                    print(colored("\nThis action will overwrite your existing changelog!\n", "yellow"))
                    input("Acknowledge..." + colored("[Enter]", f"{self.color}"))
                self.rest_bak(setting, project)

            else:
                print("")
                print(colored("Unknown option...", "light_red", attrs=["blink"]))
                time.sleep(1)

    def rest_bak(self, setting, project):
        prj_path = Path(setting.get('path'))
        has_bak = list(prj_path.glob("*.bak"))

        if not has_bak:
            print(colored(f"\nCan't find any .bak files for {project}", "yellow"))
            time.sleep(2)
            return

        bak = has_bak[0]
        bak.rename(prj_path / "CHANGELOG.md")
        print(f"\nRenamed {bak.name} to CHANGELOG.md")
        time.sleep(1)
        return
        
if __name__ == "__main__":
    ProjectsManager(config, color, header, cls, user_path)
