import configparser
from pathlib import Path

class ConfigManager:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        
        ROOT = Path(__file__).resolve().parents[1]
        
        #== Update last_project in memory.ini: ==
        self.update_last_project = Path(config_file).stem
        #== ini paths: ==
        self.memory_ini = ROOT / 'memory.ini'
        self.ini_path = ROOT / config_file
        self.new_project_ini = ROOT / "Projects" / config_file

        self.config.read(self.ini_path)
        
    def load_memory(self):
        prj = self.config['ITEMS']
        return {
            'last_project': prj.get('last_project'),
            'pinned_project': prj.get('pinned_project'),
            'pinned_project1': prj.get('pinned_project1'),
            'pinned_project2': prj.get('pinned_project2'),
            'intro': self.config.get("CONFIG", "intro"),
            'color': self.config.get("CONFIG", "color")
        }

    def update_memory(self, category: str, variable: str, value: str):
        memory_parser = configparser.ConfigParser()
        memory_parser.read(self.memory_ini)

        memory_parser.set(category, variable, value)
        with open(self.memory_ini, "w", encoding="utf-8") as f:
            memory_parser.write(f)
        return
        
    def project_ini(self):
        #==Create new project ini==
        project_parser = configparser.ConfigParser()
        project_parser["SETTINGS"] = self.data
        
        with open(self.new_project_ini, "w", encoding="utf-8") as f:
            project_parser.write(f)
            
        #==Update last_project in memory.ini==
        memory_parser = configparser.ConfigParser()
        memory_parser.read(self.memory_ini)
        
        memory_parser.set("ITEMS", "last_project", self.update_last_project)
        with open(self.memory_ini, "w", encoding="utf-8") as f:
            memory_parser.write(f)
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
        with open(self.new_project_ini, "w", encoding="utf-8") as f:
            project_parser.write(f)
        return

if __name__ == "__main__":
    ConfigManager()
