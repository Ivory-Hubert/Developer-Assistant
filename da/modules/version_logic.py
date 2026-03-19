import os, sys
import time
import subprocess
import platform
import shutil
from datetime import datetime
from pathlib import Path
import tempfile

from termcolor import colored
from prompt_toolkit import prompt
from rich.console import Console
from rich.markdown import Markdown

from da.modules.config_manager import ConfigManager
from da.modules.opener import Opener

class VersionLogic:
    def __init__(self, config, color, header, cls, user_path):
        self.config = config
        self.color = color
        self.header = header
        self.clear = cls
        self.user_path = user_path

        self.memory = self.config.load_memory()
        self.console = Console()
    
    def project_menu(self, project, profile):
        self.active_project = project
        self.active_profile = profile

        load_manager = ConfigManager(f"{project}.ini", profile=self.active_profile)

        now = datetime.now()
        self.today = now.strftime("%Y-%m-%d")

        ROOT = Path(__file__).resolve().parents[1]
        self.templog_path = ROOT / "CHANGELOG.tmp"

        no_path = colored("\nSystem cannot find the changelog path.", "light_red")

        while True:
            self.setting = load_manager.load_project()
            self.changelog_path = Path(self.setting.get('changelog'))
            self.prj_ver = self.setting.get('version')
            self.prj_path = Path(self.setting.get('path'))

            os.system(self.clear)
            print(colored(f"{self.active_profile}", f"{self.color}") + " / Main menu / Projects / Project menu / Changelog")
            print(self.header)
            print("E. Back\n")
            print(colored("Chosen project:", attrs=["underline"]))
            print(colored(self.active_project, f"{self.color}"))
            print("Version: " + colored(self.prj_ver, f"{self.color}"))
            print("\n1. Format & commit")
            print("2. Add new changes")
            print("\n3. Open the changelog")
            print("4. Preview .md changelog\n")

            choice = input(f"{self.user_path}> ").strip()

            if choice.lower() == "e":
                return

            elif choice == "1":
                if not os.path.exists(self.changelog_path):
                    print(no_path)
                    time.sleep(1)
                else:
                    self.finalise()

            elif choice == "2":
                if not os.path.exists(self.prj_path):
                    print(colored("\nSystem cannot find the path to this project.", "light_red"))
                    time.sleep(1)
                else:
                    self.update_changelog()

            elif choice == "3":
                if not os.path.exists(self.changelog_path):
                    print(no_path)
                    time.sleep(1)
                    continue
                else:
                    method = self.check_size()
                    if method == "reject":
                        continue
                    else:
                        Opener.open(self.changelog_path)

            elif choice == "4":
                if not os.path.exists(self.changelog_path):
                    print(no_path)
                    time.sleep(1)
                else:
                    log_content = ""
                    with open(self.changelog_path, "r", encoding="utf-8") as f:
                        log_content = f.read()
                    self.view_md(log_content)

            else:
                print("")
                print(colored("Unknown option...", "light_red", attrs=["bold"]))
                time.sleep(1)
            
    def finalise(self):
        with open(self.changelog_path, "r", encoding="utf-8") as f:
            existing = f.read()

        template = self.template_loader("changelog_template.txt")

        combined = template + "\n" + existing

        prj_dir = self.changelog_path.parent
        fd, temp_path = tempfile.mkstemp(dir=prj_dir, text=True)

        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(combined)
                f.flush()

            os.replace(temp_path, self.changelog_path)

        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e

        cmd = self.setting.get('command')

        if cmd.strip():
            print("\nwill run: " + colored(f"{cmd}", f"{self.color}"))
            print("in folder: " + colored(f"{self.prj_path}", f"{self.color}"))
            confirm = input("\nConfirm[Enter] or abort[E] > ").strip()
            print("")

            if confirm.lower() == "e":
                return
            try:
                subprocess.run(cmd, cwd=self.prj_path, shell=True, check=True)
            except Exception as e:
                print(colored("\nfailed: ", "light_red") + f"{e}")
                input("\nReturn...[Enter]")

        last_project = self.memory.get('last_project')
        if last_project != self.active_project:
            self.config.update_memory("ITEMS", "last_project", self.active_project)

        return

    def update_changelog(self):
        if os.path.exists(self.changelog_path):
            method = self.check_size()
            if method == "reject":
                return

        self.change_type = None
        self.change = None
        self.comment = None
        while True:
            os.system(self.clear)
            print(colored(f"{self.active_profile}", f"{self.color}") + " / Main menu / Projects / Project menu / Changelog / Add changes")
            print(self.header)
            print("E. Back/abort")
            print("O. Open templog for fixes")
            print("S. Review changes & save\n")

            print(colored("Chosen project:", attrs=["underline"]))
            print(colored(self.active_project, f"{self.color}"))
            print("Version: " + colored(self.prj_ver, f"{self.color}"))

            print(colored("\nChoose the change type:", f"{self.color}"))
            print("1. Added")
            print("2. Removed")
            print("3. Fixed")
            print("4. Changed")
            print("5. Deprecated")
            print("6. Security\n")

            print(colored("Last changelog entry:", f"{self.color}"))
            if not self.change_type:
                print("No changes yet.\n")
            else:
                print("Type: " + self.change_type)
                print("Change: " + self.change)
                print("Comment: " + self.comment + "\n")

            type_choice = input(f"{self.user_path}> ").strip()

            type_map = {
                "1": "Added",
                "2": "Removed",
                "3": "Fixed",
                "4": "Changed",
                "5": "Deprecated",
                "6": "Security"
            }

            self.change_type = type_map.get(type_choice.lower())

            if type_choice.lower() == "e":
                if os.path.exists(self.templog_path):
                    os.remove(self.templog_path)
                return
            elif type_choice in ("1", "2", "3", "4", "5", "6"):
                self.prepend_changes()
            elif type_choice.lower() == "o":
                Opener.open(self.templog_path)
            elif type_choice.lower() == "s":
                self.save_changes()
            else:
                print("")
                print(colored("Unknown option...", "light_red", attrs=["bold"]))
                time.sleep(1)

    def prepend_changes(self):
        header = f"### {self.change_type}"

        existing = ""
        if os.path.exists(self.templog_path):
            with open(self.templog_path, "r", encoding="utf-8") as f:
                existing = f.read()

        if header not in existing:
            with open(self.templog_path, "a", encoding="utf-8") as f:
                f.write(header + "\n")

        while True:
            os.system(self.clear)
            print(self.header)

            print("Chosen change type:")
            print(colored(self.change_type, f"{self.color}"))

            self.change = prompt("\nChange entry > ")

            self.comment = prompt("\nOptional comment > ")

            data = {
                "changes": self.change,
                "comments": self.comment
            }

            template = self.template_loader("entry_template.txt")

            rendered = self.template_renderer(template, data)

            with open(self.templog_path, "a", encoding="utf-8") as f:
                f.write(rendered + "\n")

            choice = input("\nNew type [E] or add more [Enter] > ")
            if choice.lower() == "e":
                return

    def save_changes(self):
        os.system(self.clear)
        print(self.header)
        print(colored("Please check the output file:", f"{self.color}", attrs=["underline"]))

        templog_content = ""
        if os.path.exists(self.templog_path):
            with open(self.templog_path, "r", encoding="utf-8") as f:
                templog_content = f.read()

            message = colored(f"[New version] - {self.today}\n", "magenta", attrs=["underline"])

            self.view_md(templog_content, message)
        else:
            print(colored("No changes added.", "light_red"))
            time.sleep(1)
            return

        choice = input("\nContinue" + colored("[Enter]", f"{self.color}") + " or add more" + colored("[E] ", f"{self.color}"))

        if choice.lower() == "e":
            return

        print("\nCurrent version: " + colored(self.prj_ver, f"{self.color}"))
        version = input("\nNew version number: ").strip()

        print("\nWorking...")

        header_data = {
            "version": version,
            "date": self.today
        }

        header_template = self.template_loader("header_template.txt")
        header_rendered = self.template_renderer(header_template, header_data)

        old_content = ""
        if os.path.exists(self.changelog_path):
            log_name = "changelog.bak"
            duplicate_path = self.prj_path / log_name

            src = self.changelog_path
            dest = duplicate_path
            shutil.copy2(src,dest)

            print("\nOld changelog backed up as: " + colored(f"{log_name}", f"{self.color}"))

            with open(self.changelog_path, "r", encoding="utf-8") as f:
                old_content = f.read()

        combined = header_rendered + "\n" + templog_content + "\n" + old_content

        log_dir = self.changelog_path.parent
        fd, temp_path = tempfile.mkstemp(dir=log_dir, text=True)

        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(combined)
                f.flush()

            os.replace(temp_path, self.changelog_path)

        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e

        os.remove(self.templog_path)

        new_config = ConfigManager(f"{self.active_project}.ini", profile=self.active_profile)
        new_config.update_project("version", version)
        new_config.update_project("edited", self.today)

        last_project = self.memory.get('last_project')
        if last_project != self.active_project:
            self.config.update_memory("ITEMS", "last_project", self.active_project)

        print(colored("\nChangelog updated, returning...", f"{self.color}"))
        time.sleep(2)
        return

    def view_md(self, log_content, message=None):
        flag = 0
        if not message:
            method = self.check_size()
            if method == "reject":
                return
            elif method == "print":
                flag = 1

        if message:
            print(message)
        else:
            os.system(self.clear)
            print(self.header)
            print("")

        if flag:
            print(log_content)
            print(colored("\nThis log is too large to render in Markdown! (Max 10MB)", "yellow"))
        else:
            md = Markdown(log_content)
            self.console.print(md)

        if not message:
            input("\nReturn..." + colored("[Enter]", f"{self.color}"))
        return

    def check_size(self):
        print_size = 10 * 1024 * 1024
        max_size = 20 * 1024 * 1024

        size = self.changelog_path.stat().st_size
        size_mb = size / (1024 * 1024)

        if size > max_size:
            print(colored(f"\nChangelog too large to load safely: {size_mb:.2f} MB", "light_red"))
            time.sleep(2)
            return "reject"

        elif size > print_size:
            return "print"

    def template_loader(self, template_file):
        template_path = self.config.templates_folder / template_file

        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()

    def template_renderer(self, template: str, data: dict):
        for key, value in data.items():
            template = template.replace(f"{{{{{key}}}}}", value)

        return template

if __name__ == "__main__":
    VersionLogic(config, color, header, cls, user_path)
