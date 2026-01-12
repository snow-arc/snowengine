import subprocess
import re
import json
from pathlib import Path
from typing import Tuple

class MPVPaperManager:
    def __init__(self, config_manager):
        self.config = config_manager
        self.monitor = config_manager.get("monitor", "*")
        self.monitor_info = self._get_monitor_info()
    
    def _get_monitor_info(self) -> dict:
        try:
            result = subprocess.run(
                ["hyprctl", "monitors", "-j"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                monitors = json.loads(result.stdout)
                if monitors:
                    return {
                        "width": monitors[0].get("width", 1920),
                        "height": monitors[0].get("height", 1080),
                        "name": monitors[0].get("name", "*"),
                        "scale": monitors[0].get("scale", 1.0)
                    }
        except:
            pass
        return {"width": 1920, "height": 1080, "name": "*", "scale": 1.0}
    
    def is_running(self) -> bool:
        try:
            result = subprocess.run(
                ["pgrep", "-x", "mpvpaper"],
                capture_output=True, text=True
            )
            return result.returncode == 0
        except:
            return False
    
    def stop(self) -> bool:
        try:
            subprocess.run(["pkill", "-9", "mpvpaper"], check=False)
            return True
        except:
            return False
    
    def _build_mpv_options(self, volume=50, loop=True, scale_mode="fill", enable_audio=True) -> list:
        options = []
        
        if loop:
            options.append("loop")
        else:
            options.append("no-loop")
        
        if scale_mode == "fill":
            options.append("--keepaspect=no")
            options.append("--video-unscaled=no")
        elif scale_mode == "fit":
            options.append("--keepaspect=yes")
            options.append("--video-unscaled=no")
        elif scale_mode == "stretch":
            options.append("--keepaspect=no")
            options.append("--video-unscaled=no")
        elif scale_mode == "center":
            options.append("--keepaspect=yes")
            options.append("--video-unscaled=yes")
        else:
            options.append("--keepaspect=no")
            options.append("--video-unscaled=no")
        
        if enable_audio:
            options.append(f"--volume={volume}")
        else:
            options.append("--no-audio")
        
        # Add panscan for better fill behavior
        options.append("--panscan=1.0")
        
        # Add video zoom and pan from config
        video_zoom = self.config.get("video_zoom", 0.0)
        pan_x = self.config.get("video_pan_x", 0.0)
        pan_y = self.config.get("video_pan_y", 0.0)
        
        if video_zoom != 0.0:
            options.append(f"--video-zoom={video_zoom:.2f}")
        if pan_x != 0.0:
            options.append(f"--video-pan-x={pan_x:.2f}")
        if pan_y != 0.0:
            options.append(f"--video-pan-y={pan_y:.2f}")
        
        return options
    
    def play(self, video_path: str, volume=50, loop=True, scale_mode="fill", enable_audio=True) -> Tuple[bool, str]:
        video_path = Path(video_path).resolve()
        
        if not video_path.exists():
            return False, f"File not found: {video_path}"
        
        self.stop()
        
        mpv_opts = self._build_mpv_options(volume, loop, scale_mode, enable_audio)
        
        # Get monitor from config
        monitor = self.config.get("monitor", "*")
        auto_pause = self.config.get("auto_pause", False)
        
        cmd = ["mpvpaper"]
        if auto_pause:
            cmd.append("-p")
        cmd.extend(["-o", " ".join(mpv_opts), monitor, str(video_path)])
        
        try:
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            return True, "Success"
        except Exception as e:
            return False, str(e)
    
    def play_youtube(self, url: str, volume=50, loop=True, scale_mode="fill", enable_audio=True) -> Tuple[bool, str]:
        if not self._validate_youtube_url(url):
            return False, "Invalid YouTube URL"
        
        if not self._check_yt_dlp():
            return False, "yt-dlp not installed"
        
        self.stop()
        
        mpv_opts = self._build_mpv_options(volume, loop, scale_mode, enable_audio)
        mpv_opts.append("--ytdl-format=bestvideo[height<=?1080]+bestaudio/best")
        
        # Get monitor from config
        monitor = self.config.get("monitor", "*")
        auto_pause = self.config.get("auto_pause", False)
        
        cmd = ["mpvpaper"]
        if auto_pause:
            cmd.append("-p")
        cmd.extend(["-o", " ".join(mpv_opts), monitor, url])
        
        try:
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            return True, "Success"
        except Exception as e:
            return False, str(e)
    
    def toggle(self) -> bool:
        if self.is_running():
            return self.stop()
        else:
            state = self.config.load_state()
            if state:
                if state["type"] == "youtube":
                    success, _ = self.play_youtube(state["current_video"])
                    return success
                else:
                    success, _ = self.play(state["current_video"])
                    return success
            return False
    
    def get_status(self):
        status = {
            "running": self.is_running(),
            "current_video": None,
            "type": None,
            "monitor": self.monitor_info
        }
        
        state = self.config.load_state()
        if state and status["running"]:
            status["current_video"] = state["current_video"]
            status["type"] = state["type"]
        
        return status
    
    def _validate_youtube_url(self, url: str) -> bool:
        patterns = [
            r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+',
        ]
        return any(re.match(pattern, url) for pattern in patterns)
    
    def _check_yt_dlp(self) -> bool:
        try:
            result = subprocess.run(
                ["which", "yt-dlp"],
                capture_output=True, text=True
            )
            return result.returncode == 0
        except:
            return False
