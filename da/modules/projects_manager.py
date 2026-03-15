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

        self.memory = self.config.load_memory()
    
    def new_project(self):
        os.system(self.cls)
        print(self.header.center(127, "="))
        print("E. Abort/back\n")
        
        name = input("Enter new project name: ")
        if name.lower() == "e":
            return

        print("")
        path = input("Enter project path: ")

        print("")
        changelog = input("Project changelog path: ")

        print("")
        version = input("Current project version: ")

        print("")
        cloud = input("Cloud service (OneDrive/Azure/Dropbox/Google Drive): ")

        print("")
        confirm = input("Confirm(Y) or abort(E): ")
        if confirm.lower() == "e":
            return
            
        elif confirm.lower() == "y":
            new_manager = ConfigManager(f"{name}.ini")
            new_manager.data = {
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
        project_ini_path = self.config.projects_folder / f"{project}.ini"
        load_manager = ConfigManager(f"{project}.ini")

        while True:
            try:
                setting = load_manager.load_project()
            except KeyError:
                print(colored(f"\nCan't find {project}.ini", "light_red"))
                time.sleep(2)
                return

            os.system(self.cls)
            print("Main menu / Projects / Project menu")
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
                version_logic.project_menu(project)

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
        has_bak = any(prj_path.glob("*.bak"))

        if not has_bak:
            print(colored(f"\nCan't find any .bak files for {project}", "yellow"))
            time.sleep(2)

        else:
            for bak in prj_path.glob("*.bak"):
                bak.rename(prj_path / "CHANGELOG.md")
                print(f"\nRenamed {bak} to CHANGELOG.md")
            time.sleep(1)
        
if __name__ == "__main__":
    ProjectsManager()
