import os
import json
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "snow-engine"
        self.config_file = self.config_dir / "config.json"
        self.state_file = self.config_dir / "state.json"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config = self.load_config()

    def load_config(self):
        default_config = {
            "volume": 50,
            "loop": True,
            "scale_mode": "fill",
            "enable_audio": True,
            "dark_mode": False,
            "video_folders": [
                str(Path.home() / "Videos"),
                str(Path.home() / "Pictures" / "Wallpapers")
            ],
            "username": "Snow",
            "avatar_path": "",
            "video_width": 1920,
            "video_height": 1080,
            "video_x": 0,
            "video_y": 0
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    saved = json.load(f)
                    default_config.update(saved)
            except:
                pass
        
        return default_config

    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=2)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

    def save_state(self, video_path, video_type):
        state = {
            "current_video": video_path,
            "type": video_type
        }
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=2)

    def load_state(self):
        if self.state_file.exists():
            try:
                with open(self.state_file, "r") as f:
                    return json.load(f)
            except:
                pass
        return None
