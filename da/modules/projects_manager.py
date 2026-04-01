import os, sys
import time
from pathlib import Path
from datetime import datetime

from prompt_toolkit import prompt
from termcolor import colored

from da.modules.config_manager import ConfigManager
from da.modules.version_logic import VersionLogic
from da.modules.opener import Opener


class ProjectsManager:
    def __init__(self, config, color, header, cls, user_path):
        self.config = config
        self.color = color
        self.header = header
        self.clear = cls
        self.user_path = user_path
    

    def projects(self, profile):
        self.active_profile = profile
        while True:
            self.memory = self.config.load_memory()
            os.system(self.clear)
            print(
                colored(f"{self.active_profile}", f"{self.color}")
                + " / Main menu / Projects"
            )
            print(self.header)
            print("Q. Back\n")

            print(colored("1. Last project:", attrs=["underline"]))
            print(colored(self.memory.get('last_project'), f"{self.color}"))

            print(colored("\nContinue a project.", attrs=["underline"]))
            print("Pinned:")
            print("a. " + colored(self.memory.get('pinned_project'), f"{self.color}"))
            print("b. " + colored(self.memory.get('pinned_project1'), f"{self.color}"))
            print("c. " + colored(self.memory.get('pinned_project2'), f"{self.color}"))

            print("\n2. Start a new project")
            print("\n3. Profile projects")

            print("")
            choice = input(f"{self.user_path}> ").strip()

            if choice.lower() == "q":
                return

            elif choice == "1":
                project = self.memory.get('last_project')
                if not project:
                    print(colored("\nLast project has not been defined...", "light_red", attrs=["bold"]))
                    time.sleep(1)
                else:
                    self.load_project(f"{project}")

            elif choice == "2":
                self.new_project()

            elif choice.lower() in ("a", "b", "c"):
                options_map = {
                    'a': 'pinned_project',
                    'b': 'pinned_project1',
                    'c': 'pinned_project2'
                }
                key = options_map.get(choice.lower())
                project_name = self.memory.get(key)
                if project_name == "":
                    print("")
                    print(colored(f"Project '{choice}' has not been defined...", "light_red", attrs=["bold"]))
                    time.sleep(1)
                else:
                    project = self.memory.get(key)
                    self.load_project(f"{project}")

            elif choice == "3":
                self.prf_projects()
            else:
                print(colored("\nUnknown option...", "light_red", attrs=["bold"]))
                time.sleep(0.5)

    def new_project(self):
        os.system(self.clear)

        now = datetime.now()
        today = now.strftime("%Y-%m-%d")

        print(self.header)
        print("Q. Abort/back")
        print("[*] - Optional\n")
        
        name = prompt("Enter new project name > ")
        if name.lower() == "q":
            return
        path = prompt("\nEnter project path > ")

        changelog = prompt("\nProject changelog path > ")

        version = prompt("\nCurrent project version > ")

        command = prompt("\nCustom commit command* > ")

        #cloud = prompt("\nCloud service* > ")

        confirm = input("\nConfirm(Y) or abort(E) > ").strip()
        if confirm.lower() == "e":
            return
            
        elif confirm.lower() == "y":
            new_manager = ConfigManager(f"{name}.ini", profile=self.active_profile)
            new_manager.data = {
                "edited" : today,
                "owner" : self.active_profile,
                "path": path,
                "changelog": changelog,
                "version": version,
                "command": command,
                "cloud": ""
            }
            new_manager.project_ini()
            return
            
        else:
            print(colored("\nUnknown option, try again...", "light_red", attrs=["bold"]))
            time.sleep(1)
            return

    def prf_projects(self):
        while True:
            os.system(self.clear)
            print(
                colored(f"{self.active_profile}", f"{self.color}")
                + " / Main menu / Projects / Profile projects"
            )
            print(self.header)
            print("Q. Back\n")
            prof_prj = self.config.projects_folder
            contents = os.listdir(prof_prj)

            projects = []

            for item in contents:
                if item.endswith(".ini"):
                    projects.append(item[:-4])

            print("Your projects:")
            for name in projects:
                print(" -" + colored(f" {name}", f"{self.color}"))

            project = input("\nProject name > ").strip()

            if project.lower() == "q":
                return
            elif project in projects:
                self.load_project(project)
            else:
                print(colored("\nInvalid name!", "light_red", attrs=["bold"]))
                time.sleep(0.5)
            
    def load_project(self, project):
        version_logic = VersionLogic(
            config=self.config,
            color=self.color,
            header=self.header,
            cls=self.clear,
            user_path=self.user_path
        )

        load_manager = ConfigManager(f"{project}.ini", profile=self.active_profile)
        project_ini_path = load_manager.projects_folder / f"{project}.ini"

        now = datetime.now()
        today = now.strftime("%Y-%m-%d")

        while True:
            try:
                setting = load_manager.load_project()
            except KeyError:
                print(colored(f"\nCan't find {project}.ini", "light_red"))
                time.sleep(0.5)
                return

            edited = setting.get('edited')
            status = self.date_math(today, edited)
            if status == "today":
                days = "today"
                suffix = ""
            elif status == "yesterday":
                days = "yesterday"
                suffix = ""
            else:
                days = status
                suffix = " days ago"

            os.system(self.clear)
            print(
                colored(f"{self.active_profile}", f"{self.color}")
                + " / Main menu / Projects / Project menu"
            )
            print(self.header)
            print("Q. Back\n")

            print(colored("Chosen project:", attrs=["underline"]))
            print(colored(project, f"{self.color}"))
            print("Last edit " + colored(days, f"{self.color}") + f"{suffix}")

            print("\n1. Open project folder")
            print("2. Manage the changelog")

            print("\n3. Open project configurations")
            print("4. Restore backup changelog\n")
            # print("5. Backup to the cloud [WIP]\n")

            choice = input(f"{self.user_path}> ").strip()

            if choice.lower() == "q":
                return

            elif choice == "1":
                folder = Path(setting.get('path'))
                Opener.open(folder)

            elif choice == "2":
                version_logic.project_menu(project, self.active_profile)

            elif choice == "3":
                Opener.open(project_ini_path)

            elif choice == "4":
                changelog = Path(setting.get('changelog'))
                if os.path.exists(changelog):
                    print(colored("\nThis action will overwrite your existing changelog!\n", "yellow", attrs=["bold"]))
                    input("Acknowledge..." + colored("[Enter]", f"{self.color}"))

                self.rest_bak(setting, changelog, project)

            #elif choice == "5":

            else:
                print(colored("\nUnknown option...", "light_red", attrs=["bold"]))
                time.sleep(1)

    def rest_bak(self, setting, changelog, project):
        prj_path = Path(setting.get('path'))
        has_bak = list(prj_path.glob("*.bak"))

        if not has_bak:
            print(colored(f"\nCan't find any .bak files for {project}", "yellow"))
            time.sleep(0.5)
            return

        bak = has_bak[0]
        os.replace(bak, changelog)
        print(f"\nReplaced {bak.name} with CHANGELOG.md")
        time.sleep(1)
        return

    def date_math(self, today, edited):
        try:
            d = datetime.strptime(today, "%Y-%m-%d").date()
            d1 = datetime.strptime(edited, "%Y-%m-%d").date()
        except Exception:
            return "?"

        dif = (d - d1).days

        if dif == 0:
            return "today"
        elif dif == 1:
            return "yesterday"
        else:
            return dif

if __name__ == "__main__":
    ProjectsManager(config, color, header, cls, user_path)
