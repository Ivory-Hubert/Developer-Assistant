import os
import configparser
from pathlib import Path
import shutil
import time
import tempfile

from platformdirs import user_config_path

from importlib import resources

class ConfigManager:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        
        self.internal_dir = Path(__file__).resolve().parents[1]
        self.global_dir = user_config_path("da-ui")
        self.global_dir.mkdir(parents=True, exist_ok=True)
        
        self.memory_ini = self.global_dir / 'memory.ini'
        self.projects_folder = self.global_dir / "Projects"
        self.templates_folder = self.global_dir / "Templates"
        self.new_project_ini = self.projects_folder / config_file

        self.update_last_project = Path(config_file).stem

    def load_memory(self):
        self.config.read(self.memory_ini)
        prj = self.config['ITEMS']
        return {
            'last_project': prj.get('last_project'),
            'pinned_project': prj.get('pinned_project'),
            'pinned_project1': prj.get('pinned_project1'),
            'pinned_project2': prj.get('pinned_project2'),
            'color': self.config.get("CONFIG", "color")
        }

    def update_memory(self, category: str, variable: str, value: str):
        memory_parser = configparser.ConfigParser()
        memory_parser.read(self.memory_ini)
        memory_parser.set(category, variable, value)

        ini_dir = self.memory_ini.parent
        fd, temp_path = tempfile.mkstemp(dir=ini_dir, text=True)

        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                memory_parser.write(f)
            os.replace(temp_path, self.memory_ini)

        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e

        return
        
    def project_ini(self):
        #==Create new project ini==
        project_parser = configparser.ConfigParser()
        project_parser["SETTINGS"] = self.data
        
        with open(self.new_project_ini, "w", encoding="utf-8") as f:
            project_parser.write(f)
            
        self.update_memory("ITEMS", "last_project", self.update_last_project)

        return
    
    def load_project(self):
        #==Return project ini variables==
        project_parser = configparser.ConfigParser()
        project_parser.read(self.new_project_ini)

        prj = project_parser['SETTINGS']
        return {
            'path': prj.get('path'),
            'changelog': prj.get('changelog'),
            'version': prj.get('version'),
            'cloud': prj.get('cloud')
        }

    def update_project(self, variable: str, value: str):
        project_parser = configparser.ConfigParser()
        project_parser.read(self.new_project_ini)
        project_parser.set("SETTINGS", variable, value)

        ini_dir = self.new_project_ini.parent
        fd, temp_path = tempfile.mkstemp(dir=ini_dir, text=True)

        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                project_parser.write(f)
            os.replace(temp_path, self.new_project_ini)

        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e

        return

    def data_check(self):
        old_memory = self.internal_dir / "memory.ini"
        old_projects = self.internal_dir / "Projects"

        messages = []

        if old_memory.exists() and not self.memory_ini.exists():
            shutil.move(str(old_memory), str(self.memory_ini))
            messages.append(f"Migrated memory.ini to {self.global_dir}")

        if old_projects.exists() and not self.projects_folder.exists():
            shutil.move(str(old_projects), str(self.projects_folder))
            messages.append(f"Migrated Projects folder to {self.global_dir}")

        if not self.templates_folder.exists():
            default_templates = resources.files("da.templates")
            user_templates = self.templates_folder

            user_templates.mkdir(parents=True, exist_ok=True)

            for item in default_templates.iterdir():
                dest = user_templates / item.name
                if not dest.exists():
                    shutil.copy(item, dest)

            messages.append(f"Copied default Templates to {self.global_dir}")

        return messages

if __name__ == "__main__":
    ConfigManager()
