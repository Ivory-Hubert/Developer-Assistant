import os, sys
import time
from termcolor import colored
import subprocess
import platform
from pathlib import Path

from da.modules.config_manager import ConfigManager
from da.modules.version_logic import VersionLogic
from da.modules.opener import Opener

class ProjectsManager:
    def __init__(self, config, color="light_blue"):
        self.config = config
        self.memory = self.config.load_memory()
        self.color = self.memory.get('color') or color
        
        #==Reusables==
        self.header = (colored(" Developer Assistant ", f"{self.color}"))
        self.clear_screen = 'cls' if platform.system() == 'Windows' else 'clear'
        self.user_path = os.environ.get('USERPROFILE') or os.environ.get('HOME', 'User')
    
    def new_project(self):
        os.system(self.clear_screen)
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
        version_logic = VersionLogic(config=self.config)
        project_ini_path = self.config.projects_folder / f"{project}.ini"
        load_manager = ConfigManager(f"{project}.ini")

        while True:
            try:
                setting = load_manager.load_project()
            except KeyError:
                print(colored(f"\nCan't find {project}.ini", "light_red"))
                time.sleep(2)
                return

            os.system(self.clear_screen)
            print("Main menu / Projects / Project menu")
            print(self.header.center(127, "="))
            print("E. Back\n")
            print(colored("Chosen project:", attrs=["underline"]))
            print(colored(project, f"{self.color}"))
            print("\n1. Open project folder.")
            print("2. Update the changelog.")
            print("3. Backup to the cloud. [WIP]")
            print("4. Open project configurations.\n")

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

            else:
                print("")
                print(colored("Unknown option...", "light_red", attrs=["blink"]))
                time.sleep(1)
        
if __name__ == "__main__":
    ProjectsManager()
