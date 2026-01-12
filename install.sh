#!/bin/bash

set -e

echo "========================"
echo "  SnowEngine Installer"
echo "========================"
echo

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
INSTALL_DIR="$HOME/.local/share/snow-engine"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "[1/4] Checking dependencies..."

MISSING=()

command -v mpvpaper &> /dev/null || MISSING+=("mpvpaper")
command -v mpv &> /dev/null || MISSING+=("mpv")
command -v python &> /dev/null || MISSING+=("python")

if ! python -c "import gi; gi.require_version('Gtk', '4.0')" 2>/dev/null; then
    MISSING+=("python-gobject gtk4")
fi

if ! python -c "import gi; gi.require_version('Adw', '1')" 2>/dev/null; then
    MISSING+=("libadwaita")
fi

if [ ${#MISSING[@]} -ne 0 ]; then
    echo "Missing:"
    printf '  - %s\n' "${MISSING[@]}"
    echo
    echo "Install: sudo pacman -S mpvpaper mpv python python-gobject gtk4 libadwaita"
    exit 1
fi

command -v yt-dlp &> /dev/null && echo "yt-dlp: OK" || echo "yt-dlp: Not found (YouTube disabled)"

echo
echo "[2/4] Installing..."
mkdir -p "$INSTALL_DIR" "$BIN_DIR" "$DESKTOP_DIR"

rm -rf "$INSTALL_DIR/src"
cp -r "$SCRIPT_DIR/src" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/video-wallpaper" "$INSTALL_DIR/snow-engine"
cp "$SCRIPT_DIR/video-wallpaper-cli" "$INSTALL_DIR/snow-engine-cli"
chmod +x "$INSTALL_DIR/snow-engine" "$INSTALL_DIR/snow-engine-cli"

echo
echo "[3/4] Creating shortcuts..."
ln -sf "$INSTALL_DIR/snow-engine" "$BIN_DIR/snow-engine"
ln -sf "$INSTALL_DIR/snow-engine-cli" "$BIN_DIR/snow-engine-cli"

cat > "$DESKTOP_DIR/snow-engine.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=SnowEngine
Comment=Video Wallpaper Manager
Icon=video-display
Exec=$INSTALL_DIR/snow-engine
Terminal=false
Categories=Utility;GTK;
EOF

chmod +x "$DESKTOP_DIR/snow-engine.desktop"

echo
echo "[4/4] Adding keybind..."
HYPR_CONF="$HOME/.config/hypr/hyprland.conf"

if [ -f "$HYPR_CONF" ]; then
    if ! grep -q "snow-engine" "$HYPR_CONF"; then
        echo "" >> "$HYPR_CONF"
        echo "# SnowEngine" >> "$HYPR_CONF"
        echo "bind = CTRL SHIFT, D, exec, $INSTALL_DIR/snow-engine" >> "$HYPR_CONF"
        echo "Keybind added: Ctrl+Shift+D"
    else
        echo "Keybind exists"
    fi
fi

echo
echo "========================"
echo "  Done!"
echo "========================"
echo "Run: snow-engine"
echo "Or press: Ctrl+Shift+D"
