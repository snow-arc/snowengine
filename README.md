# ❄️ SnowEngine

A beautiful video wallpaper manager for Hyprland/Wayland.

![License](https://img.shields.io/badge/license-GPL--3.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![GTK](https://img.shields.io/badge/GTK-4.0-orange)

## ✨ Features

### Video Playback
- 🎬 Local video files (MP4, WebM, MKV, AVI, MOV, GIF)
- 📺 YouTube video streaming support
- 🔁 Loop playback option
- 🔊 Volume control with audio toggle

### Display Settings
- 📐 Multiple scaling modes (Fill, Fit, Stretch, Center)
- 🖥️ Multi-monitor support (All monitors or specific)
- 🔍 Video zoom control
- ↔️ Pan X/Y positioning

### User Interface
- 🌙 Dark/Light theme toggle
- 📁 Multiple video folder support
- 🗑️ Remove videos from list (without deleting files)
- 🔄 Auto-refresh video library
- ⏸️ Auto-pause when window focused

### Settings
- 👤 Custom username
- 🖼️ Custom avatar image (ok i remove this, no need for it, i forget about that)
- 💾 Persistent configuration

## 📋 Requirements

### Core Dependencies
- `mpvpaper` - Video wallpaper backend
- `mpv` - Media player
- `python` >= 3.10
- `python-gobject` - GTK bindings
- `gtk4` - GTK4 library
- `libadwaita` - Adwaita widgets

### Optional
- `yt-dlp` - YouTube streaming support
- `ffmpeg` - Video thumbnail generation

## 🚀 Installation

### Arch Linux

```bash
# Install dependencies
sudo pacman -S mpvpaper mpv python python-gobject gtk4 libadwaita ffmpeg yt-dlp

# Clone and install
git clone https://github.com/snow/snow-engine.git
cd snow-engine
./install.sh
```

### Manual Installation

```bash
./install.sh
```

This will:
- Copy files to `~/.local/share/snow-engine/`
- Create desktop entry
- Add `Ctrl+Shift+D` keybind to Hyprland config

## 💻 Usage

### Launch Application
```bash
snow-engine
```

### Keyboard Shortcut
Press `Ctrl+Shift+D` to launch SnowEngine (Hyprland)

### CLI Mode
```bash
snow-engine-cli --video /path/to/video.mp4
snow-engine-cli --youtube "https://youtube.com/watch?v=..."
snow-engine-cli --stop
```

## 📁 Project Structure

```
snow-engine/
├── video-wallpaper          # Main entry point
├── video-wallpaper-cli      # CLI entry point
├── install.sh               # Installation script
├── README.md
└── src/
    ├── core/
    │   ├── config.py        # Configuration manager
    │   └── mpvpaper.py      # mpvpaper control
    ├── ui/
    │   └── main_window.py   # Main application UI
    └── assets/
        └── styles/
            └── pixel_theme.py  # Dark/Light CSS themes
```

## ⚙️ Configuration

Configuration is stored in `~/.config/snow-engine/config.json`

```json
{
  "video_folders": ["/path/to/videos"],
  "volume": 50,
  "loop": true,
  "scale_mode": "fill",
  "enable_audio": true,
  "dark_mode": true,
  "username": "Snow",
  "hidden_videos": []
}
```

## 🎨 Theming

SnowEngine includes beautiful dark and light themes with:
- Gradient backgrounds
- Smooth animations
- Modern rounded design
- Purple/Pink accent colors

## 🛠️ Uninstall

```bash
rm -rf ~/.local/share/snow-engine
rm ~/.local/bin/snow-engine
rm ~/.local/bin/snow-engine-cli
rm ~/.local/share/applications/snow-engine.desktop
```

## 📝 License

GPL-3.0

---

Made with ❄️ by Snow
