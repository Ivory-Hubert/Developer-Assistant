import os, sys
import time
from termcolor import colored
import subprocess
import platform
from pathlib import Path
from Modules.config_manager import ConfigManager
from Modules.version_logic import VersionLogic
from Modules.opener import Opener

class ProjectsManager:
    def __init__(self, color="light_blue"):
        os.system('title Developer Assistant')
        self.version = "1.0.0-alpha"
        
        self.config = ConfigManager('memory.ini')
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
        # save ini name
        print("")
        path = input("Enter project path: ")
        # save to ini
        print("")
        changelog = input("Project changelog path: ")
        # save to ini
        print("")
        version = input("Current project version: ")
        # save to ini
        print("")
        cloud = input("Cloud service (OneDrive/Azure/Dropbox/Google Drive): ")
        # save to ini
        print("")
        confirm = input("Confirm(Y) or abort(E): ")
        if confirm.lower() == "e":
            return
            
        elif confirm.lower() == "y":
            self.new_manager = ConfigManager(f"{name}.ini")
            self.new_manager.data = {
                "path": path,
                "changelog": changelog,
                "version": version,
                "cloud": cloud
            }
            self.new_manager.project_ini()

            return
            
        else:
            print("")
            print(colored("Unknown option, try again...", "light_red", attrs=["blink"]))
            time.sleep(2)
            return
            
    def load_project(self, project):
        while True:
            chosen_project = f"{project}"
            self.load_manager = ConfigManager(f"{project}.ini")
            self.setting = self.load_manager.load_project()
            self.version_logic = VersionLogic()

            ROOT = Path(__file__).resolve().parents[1]
            project_ini_path = ROOT / "Projects" / f"{chosen_project}.ini"

            os.system(self.clear_screen)
            print("Main menu / Projects / Project menu")
            print(self.header.center(127, "="))
            print("E. Back\n")
            print(colored("Chosen project:", attrs=["underline"]))
            print(colored(chosen_project, f"{self.color}"))
            print("\n1. Open project folder.")
            print("2. Update the changelog.")
            print("3. Backup to the cloud. [X]")
            print("4. Open project configurations.\n")

            choice = input(f"{self.user_path}> ").strip()

            if choice.lower() == "e":
                return

            elif choice == "1":
                path = self.setting.get('path')
                folder = Path(path)
                Opener.open(folder)

            elif choice == "2":
                self.version_logic.project_menu(chosen_project)

            # elif choice == "3":

            elif choice == "4":
                Opener.open(project_ini_path)

            else:
                print("")
                print(colored("Unknown option...", "light_red", attrs=["blink"]))
                time.sleep(2)
        
if __name__ == "__main__":
    ProjectsManager()
