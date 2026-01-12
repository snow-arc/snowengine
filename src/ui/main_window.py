import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio, Gdk, GdkPixbuf
import os
import subprocess
import json
from src.core.config import ConfigManager
from src.core.mpvpaper import MPVPaperManager
from src.assets.styles.pixel_theme import apply_theme


class MainWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.config_manager = ConfigManager()
        self.mpvpaper = MPVPaperManager(self.config_manager)
        self.selected_wallpaper = None
        self.current_page = "local"
        self.css_provider = None
        
        self.set_title("SnowEngine")
        self.set_default_size(900, 600)
        self.set_size_request(600, 400)  # Minimum size
        
        self.apply_current_theme()
        self.setup_ui()
        self.load_wallpapers()
        self.update_status()
        self.update_preview()
        
        GLib.timeout_add(2000, self.update_status)
    
    def apply_current_theme(self):
        dark_mode = self.config_manager.get("dark_mode", True)
        self.css_provider = apply_theme(dark_mode)
    
    def setup_ui(self):
        # Main scrollable container for responsiveness
        main_scroll = Gtk.ScrolledWindow()
        main_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.add_css_class("main-container")
        main_box.set_margin_top(12)
        main_box.set_margin_bottom(12)
        main_box.set_margin_start(12)
        main_box.set_margin_end(12)
        
        sidebar = self.create_sidebar()
        main_box.append(sidebar)
        
        self.content_stack = Gtk.Stack()
        self.content_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.content_stack.set_hexpand(True)
        self.content_stack.set_vexpand(True)
        
        local_page = self.create_local_page()
        self.content_stack.add_named(local_page, "local")
        
        settings_page = self.create_settings_page()
        self.content_stack.add_named(settings_page, "settings")
        
        main_box.append(self.content_stack)
        
        right_panel = self.create_right_panel()
        main_box.append(right_panel)
        
        main_scroll.set_child(main_box)
        self.set_content(main_scroll)
    
    def create_sidebar(self):
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar.add_css_class("sidebar")
        sidebar.set_size_request(130, -1)
        sidebar.set_vexpand(True)
        
        # Snowflake Logo Header
        header = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        header.add_css_class("sidebar-header")
        header.set_halign(Gtk.Align.CENTER)
        header.set_margin_top(15)
        header.set_margin_bottom(15)
        
        # Snowflake icon
        snow_icon = Gtk.Label(label="❄")
        snow_icon.add_css_class("snow-logo")
        header.append(snow_icon)
        
        # "Snow" text
        snow_label = Gtk.Label(label="Snow")
        snow_label.add_css_class("snow-title")
        header.append(snow_label)
        
        # "Engine" text
        engine_label = Gtk.Label(label="Engine")
        engine_label.add_css_class("snow-subtitle")
        header.append(engine_label)
        
        sidebar.append(header)
        
        # Menu Label
        menu_label = Gtk.Label(label="Menu")
        menu_label.add_css_class("menu-label")
        menu_label.set_halign(Gtk.Align.START)
        menu_label.set_margin_start(12)
        menu_label.set_margin_top(10)
        sidebar.append(menu_label)
        
        # Local button
        self.local_btn = self.create_menu_item("folder-videos-symbolic", "Local", True)
        self.local_btn.connect("clicked", lambda b: self.switch_page("local"))
        sidebar.append(self.local_btn)
        
        # Settings button
        self.settings_btn = self.create_menu_item("emblem-system-symbolic", "Settings", False)
        self.settings_btn.connect("clicked", lambda b: self.switch_page("settings"))
        sidebar.append(self.settings_btn)
        
        # Spacer
        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        sidebar.append(spacer)
        
        # Branding
        branding = Gtk.Label(label="Snow")
        branding.add_css_class("app-branding")
        branding.set_halign(Gtk.Align.START)
        branding.set_margin_start(12)
        branding.set_margin_bottom(12)
        sidebar.append(branding)
        
        return sidebar
    
    def create_menu_item(self, icon_name, label_text, active=False):
        button = Gtk.Button()
        button.add_css_class("menu-item")
        if active:
            button.add_css_class("active")
        
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        icon = Gtk.Image.new_from_icon_name(icon_name)
        icon.add_css_class("menu-icon")
        box.append(icon)
        
        label = Gtk.Label(label=label_text)
        box.append(label)
        
        button.set_child(box)
        return button
    
    def switch_page(self, page):
        self.current_page = page
        self.content_stack.set_visible_child_name(page)
        
        self.local_btn.remove_css_class("active")
        self.settings_btn.remove_css_class("active")
        
        if page == "local":
            self.local_btn.add_css_class("active")
        elif page == "settings":
            self.settings_btn.add_css_class("active")
    
    def create_local_page(self):
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        content.add_css_class("content-area")
        
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        header.add_css_class("feeds-header")
        header.set_margin_bottom(12)
        
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        title = Gtk.Label(label="Local Videos")
        title.add_css_class("feeds-title")
        title.set_halign(Gtk.Align.START)
        title_box.append(title)
        
        self.video_count_label = Gtk.Label(label="")
        self.video_count_label.add_css_class("video-count")
        title_box.append(self.video_count_label)
        header.append(title_box)
        
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        header.append(spacer)
        
        refresh_btn = Gtk.Button(label="↻ Refresh")
        refresh_btn.add_css_class("refresh-button")
        refresh_btn.connect("clicked", self.on_refresh_clicked)
        header.append(refresh_btn)
        
        folder_btn = Gtk.Button(label="📁 Add Folder")
        folder_btn.add_css_class("folder-button")
        folder_btn.set_margin_start(6)
        folder_btn.connect("clicked", self.on_open_folder_clicked)
        header.append(folder_btn)
        
        content.append(header)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)
        
        self.wallpaper_grid = Gtk.FlowBox()
        self.wallpaper_grid.set_valign(Gtk.Align.START)
        self.wallpaper_grid.set_halign(Gtk.Align.FILL)
        self.wallpaper_grid.set_max_children_per_line(10)
        self.wallpaper_grid.set_min_children_per_line(1)
        self.wallpaper_grid.set_column_spacing(12)
        self.wallpaper_grid.set_row_spacing(12)
        self.wallpaper_grid.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.wallpaper_grid.add_css_class("wallpaper-grid")
        self.wallpaper_grid.set_homogeneous(False)
        self.wallpaper_grid.connect("child-activated", self.on_wallpaper_selected)
        
        scrolled.set_child(self.wallpaper_grid)
        content.append(scrolled)
        
        return content
    
    def create_settings_page(self):
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        content.add_css_class("content-area")
        
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        header.add_css_class("feeds-header")
        header.set_margin_bottom(12)
        
        title = Gtk.Label(label="Settings")
        title.add_css_class("feeds-title")
        title.set_halign(Gtk.Align.START)
        header.append(title)
        
        content.append(header)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        
        settings_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        settings_box.set_margin_end(10)
        
        # Display Settings Section
        display_section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        display_section.add_css_class("settings-section")
        
        display_title = Gtk.Label(label="Display Settings")
        display_title.add_css_class("settings-title")
        display_title.set_halign(Gtk.Align.START)
        display_section.append(display_title)
        
        # Monitor Selection
        monitor_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        monitor_label = Gtk.Label(label="Monitor")
        monitor_label.add_css_class("control-label")
        monitor_row.append(monitor_label)
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        monitor_row.append(spacer)
        
        self.monitor_combo = Gtk.ComboBoxText()
        self.monitor_combo.append("*", "All Monitors")
        for mon in self.get_monitors():
            self.monitor_combo.append(mon, mon)
        self.monitor_combo.set_active_id(self.config_manager.get("monitor", "*"))
        self.monitor_combo.add_css_class("scale-dropdown")
        self.monitor_combo.connect("changed", self.on_monitor_changed)
        monitor_row.append(self.monitor_combo)
        display_section.append(monitor_row)
        
        # Video Zoom (Scale)
        zoom_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        zoom_label = Gtk.Label(label="Video Zoom")
        zoom_label.add_css_class("control-label")
        zoom_row.append(zoom_label)
        spacer2 = Gtk.Box()
        spacer2.set_hexpand(True)
        zoom_row.append(spacer2)
        
        self.zoom_spin = Gtk.SpinButton.new_with_range(-1.0, 2.0, 0.1)
        self.zoom_spin.set_value(self.config_manager.get("video_zoom", 0.0))
        self.zoom_spin.set_digits(1)
        self.zoom_spin.add_css_class("spin-entry")
        self.zoom_spin.connect("value-changed", self.on_zoom_changed)
        zoom_row.append(self.zoom_spin)
        display_section.append(zoom_row)
        
        # Video Pan X
        pan_x_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        pan_x_label = Gtk.Label(label="Pan X")
        pan_x_label.add_css_class("control-label")
        pan_x_row.append(pan_x_label)
        spacer3 = Gtk.Box()
        spacer3.set_hexpand(True)
        pan_x_row.append(spacer3)
        
        self.pan_x_spin = Gtk.SpinButton.new_with_range(-1.0, 1.0, 0.05)
        self.pan_x_spin.set_value(self.config_manager.get("video_pan_x", 0.0))
        self.pan_x_spin.set_digits(2)
        self.pan_x_spin.add_css_class("spin-entry")
        self.pan_x_spin.connect("value-changed", self.on_pan_changed)
        pan_x_row.append(self.pan_x_spin)
        display_section.append(pan_x_row)
        
        # Video Pan Y
        pan_y_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        pan_y_label = Gtk.Label(label="Pan Y")
        pan_y_label.add_css_class("control-label")
        pan_y_row.append(pan_y_label)
        spacer4 = Gtk.Box()
        spacer4.set_hexpand(True)
        pan_y_row.append(spacer4)
        
        self.pan_y_spin = Gtk.SpinButton.new_with_range(-1.0, 1.0, 0.05)
        self.pan_y_spin.set_value(self.config_manager.get("video_pan_y", 0.0))
        self.pan_y_spin.set_digits(2)
        self.pan_y_spin.add_css_class("spin-entry")
        self.pan_y_spin.connect("value-changed", self.on_pan_changed)
        pan_y_row.append(self.pan_y_spin)
        display_section.append(pan_y_row)
        
        # Auto-Pause Toggle
        pause_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        pause_label = Gtk.Label(label="Auto-Pause")
        pause_label.add_css_class("control-label")
        pause_row.append(pause_label)
        spacer5 = Gtk.Box()
        spacer5.set_hexpand(True)
        pause_row.append(spacer5)
        
        self.autopause_switch = Gtk.Switch()
        self.autopause_switch.set_active(self.config_manager.get("auto_pause", False))
        self.autopause_switch.connect("state-set", self.on_autopause_changed)
        pause_row.append(self.autopause_switch)
        display_section.append(pause_row)
        
        settings_box.append(display_section)
        
        # Appearance Section
        appearance_section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        appearance_section.add_css_class("settings-section")
        
        appearance_title = Gtk.Label(label="Appearance")
        appearance_title.add_css_class("settings-title")
        appearance_title.set_halign(Gtk.Align.START)
        appearance_section.append(appearance_title)
        
        dark_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        dark_label = Gtk.Label(label="Dark Mode")
        dark_label.add_css_class("control-label")
        dark_row.append(dark_label)
        spacer6 = Gtk.Box()
        spacer6.set_hexpand(True)
        dark_row.append(spacer6)
        
        self.dark_switch = Gtk.Switch()
        self.dark_switch.set_active(self.config_manager.get("dark_mode", True))
        self.dark_switch.connect("state-set", self.on_dark_mode_changed)
        dark_row.append(self.dark_switch)
        appearance_section.append(dark_row)
        
        settings_box.append(appearance_section)
        
        # Profile Section
        profile_section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        profile_section.add_css_class("settings-section")
        
        profile_title = Gtk.Label(label="Profile")
        profile_title.add_css_class("settings-title")
        profile_title.set_halign(Gtk.Align.START)
        profile_section.append(profile_title)
        
        name_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        name_label = Gtk.Label(label="Username")
        name_label.add_css_class("control-label")
        name_row.append(name_label)
        spacer7 = Gtk.Box()
        spacer7.set_hexpand(True)
        name_row.append(spacer7)
        
        self.username_entry = Gtk.Entry()
        self.username_entry.set_text(self.config_manager.get("username", "Snow"))
        self.username_entry.add_css_class("url-entry")
        self.username_entry.set_max_width_chars(15)
        self.username_entry.connect("changed", self.on_username_changed)
        name_row.append(self.username_entry)
        profile_section.append(name_row)
        
        avatar_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        avatar_label = Gtk.Label(label="Avatar")
        avatar_label.add_css_class("control-label")
        avatar_row.append(avatar_label)
        spacer8 = Gtk.Box()
        spacer8.set_hexpand(True)
        avatar_row.append(spacer8)
        
        avatar_btn = Gtk.Button(label="Choose Image")
        avatar_btn.add_css_class("folder-button")
        avatar_btn.connect("clicked", self.on_choose_avatar)
        avatar_row.append(avatar_btn)
        profile_section.append(avatar_row)
        
        settings_box.append(profile_section)
        
        scrolled.set_child(settings_box)
        content.append(scrolled)
        
        return content
    
    def get_monitors(self):
        """Get available monitors using hyprctl"""
        monitors = []
        try:
            result = subprocess.run(
                ["hyprctl", "monitors", "-j"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                for mon in data:
                    monitors.append(mon.get("name", ""))
        except:
            pass
        return monitors
    
    def on_monitor_changed(self, combo):
        monitor = combo.get_active_id() or "*"
        self.config_manager.set("monitor", monitor)
    
    def on_zoom_changed(self, spin):
        self.config_manager.set("video_zoom", spin.get_value())
    
    def on_pan_changed(self, spin):
        self.config_manager.set("video_pan_x", self.pan_x_spin.get_value())
        self.config_manager.set("video_pan_y", self.pan_y_spin.get_value())
    
    def on_autopause_changed(self, switch, state):
        self.config_manager.set("auto_pause", state)
        return False
    
    def create_right_panel(self):
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_size_request(280, -1)
        
        panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        panel.add_css_class("right-panel")
        panel.set_margin_start(12)
        panel.set_vexpand(True)
        
        # Top Bar with Settings Button (NO search box)
        top_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        top_bar.set_margin_bottom(10)
        
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        top_bar.append(spacer)
        
        settings_btn = Gtk.Button()
        settings_btn.set_child(Gtk.Image.new_from_icon_name("emblem-system-symbolic"))
        settings_btn.add_css_class("icon-button")
        settings_btn.add_css_class("primary")
        settings_btn.connect("clicked", lambda b: self.switch_page("settings"))
        top_bar.append(settings_btn)
        
        panel.append(top_bar)
        
        # Preview Card - compact design
        preview_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        preview_card.add_css_class("preview-card")
        preview_card.set_halign(Gtk.Align.CENTER)
        
        self.preview_image_box = Gtk.Box()
        self.preview_image_box.add_css_class("preview-image")
        self.preview_image_box.set_halign(Gtk.Align.CENTER)
        self.preview_image_widget = None
        
        preview_card.append(self.preview_image_box)
        
        # Title and Apply in same row
        title_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        title_row.set_halign(Gtk.Align.CENTER)
        
        self.title_label = Gtk.Label(label="Select Video")
        self.title_label.add_css_class("preview-title")
        title_row.append(self.title_label)
        
        self.apply_btn = Gtk.Button(label="Apply")
        self.apply_btn.add_css_class("apply-btn")
        self.apply_btn.connect("clicked", self.on_apply_clicked)
        title_row.append(self.apply_btn)
        
        preview_card.append(title_row)
        panel.append(preview_card)
        
        # Controls Box
        controls_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        controls_box.set_margin_top(16)
        
        # Scale Row
        scale_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        scale_icon = Gtk.Image.new_from_icon_name("zoom-fit-best-symbolic")
        scale_row.append(scale_icon)
        scale_label = Gtk.Label(label="Scale")
        scale_label.add_css_class("control-label")
        scale_row.append(scale_label)
        scale_spacer = Gtk.Box()
        scale_spacer.set_hexpand(True)
        scale_row.append(scale_spacer)
        
        self.scale_combo = Gtk.ComboBoxText()
        self.scale_combo.append("fill", "Fill")
        self.scale_combo.append("fit", "Fit")
        self.scale_combo.append("stretch", "Stretch")
        self.scale_combo.append("center", "Center")
        self.scale_combo.set_active_id(self.config_manager.get("scale_mode", "fill"))
        self.scale_combo.add_css_class("scale-dropdown")
        scale_row.append(self.scale_combo)
        controls_box.append(scale_row)
        
        # Volume Row
        volume_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        volume_icon = Gtk.Image.new_from_icon_name("audio-volume-high-symbolic")
        volume_row.append(volume_icon)
        volume_label = Gtk.Label(label="Volume")
        volume_label.add_css_class("control-label")
        volume_row.append(volume_label)
        volume_spacer = Gtk.Box()
        volume_spacer.set_hexpand(True)
        volume_row.append(volume_spacer)
        
        self.volume_slider = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 5)
        self.volume_slider.set_value(self.config_manager.get("volume", 50))
        self.volume_slider.set_size_request(100, -1)
        self.volume_slider.add_css_class("control-slider")
        volume_row.append(self.volume_slider)
        controls_box.append(volume_row)
        
        # Audio Row
        audio_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        audio_icon = Gtk.Image.new_from_icon_name("audio-speakers-symbolic")
        audio_row.append(audio_icon)
        audio_label = Gtk.Label(label="Audio")
        audio_label.add_css_class("control-label")
        audio_row.append(audio_label)
        audio_spacer = Gtk.Box()
        audio_spacer.set_hexpand(True)
        audio_row.append(audio_spacer)
        
        self.audio_switch = Gtk.Switch()
        self.audio_switch.set_active(self.config_manager.get("enable_audio", True))
        audio_row.append(self.audio_switch)
        controls_box.append(audio_row)
        
        # Loop Row
        loop_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        loop_icon = Gtk.Image.new_from_icon_name("media-playlist-repeat-symbolic")
        loop_row.append(loop_icon)
        loop_label = Gtk.Label(label="Loop")
        loop_label.add_css_class("control-label")
        loop_row.append(loop_label)
        loop_spacer = Gtk.Box()
        loop_spacer.set_hexpand(True)
        loop_row.append(loop_spacer)
        
        self.loop_switch = Gtk.Switch()
        self.loop_switch.set_active(self.config_manager.get("loop", True))
        loop_row.append(self.loop_switch)
        controls_box.append(loop_row)
        
        panel.append(controls_box)
        
        # YouTube Section
        url_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        url_box.set_margin_top(16)
        
        url_label = Gtk.Label(label="YouTube URL")
        url_label.add_css_class("control-label")
        url_label.set_halign(Gtk.Align.START)
        url_box.append(url_label)
        
        self.url_entry = Gtk.Entry()
        self.url_entry.set_placeholder_text("Paste URL...")
        self.url_entry.add_css_class("url-entry")
        url_box.append(self.url_entry)
        
        yt_btn = Gtk.Button(label="▶ Play YouTube")
        yt_btn.add_css_class("play-button")
        yt_btn.set_margin_top(5)
        yt_btn.connect("clicked", self.on_youtube_clicked)
        url_box.append(yt_btn)
        
        panel.append(url_box)
        
        # Spacer
        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        panel.append(spacer)
        
        # Footer - minimal status bar
        footer_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        footer_box.add_css_class("panel-footer")
        
        # Left side - Snow branding
        snow_label = Gtk.Label(label="❄ Snow")
        snow_label.add_css_class("footer-brand")
        footer_box.append(snow_label)
        
        # Center spacer
        footer_spacer = Gtk.Box()
        footer_spacer.set_hexpand(True)
        footer_box.append(footer_spacer)
        
        # Right side - status and stop button
        self.status_label = Gtk.Label(label="● Stopped")
        self.status_label.add_css_class("status-stopped")
        footer_box.append(self.status_label)
        
        stop_btn = Gtk.Button(label="Stop")
        stop_btn.add_css_class("mini-stop-button")
        stop_btn.connect("clicked", self.on_stop_clicked)
        footer_box.append(stop_btn)
        
        panel.append(footer_box)
        
        scrolled.set_child(panel)
        return scrolled
    
    def load_wallpapers(self):
        while True:
            child = self.wallpaper_grid.get_first_child()
            if child is None:
                break
            self.wallpaper_grid.remove(child)
        
        folders = self.config_manager.get("video_folders", [])
        hidden_videos = self.config_manager.get("hidden_videos", [])
        self.wallpapers = []
        
        video_extensions = ('.mp4', '.webm', '.mkv', '.avi', '.mov', '.gif')
        
        for directory in folders:
            if os.path.exists(directory):
                try:
                    for f in os.listdir(directory):
                        if f.lower().endswith(video_extensions):
                            full_path = os.path.join(directory, f)
                            # Skip hidden videos
                            if full_path in hidden_videos:
                                continue
                            self.wallpapers.append({
                                'name': os.path.splitext(f)[0],
                                'path': full_path,
                                'type': 'local'
                            })
                except:
                    pass
        
        # Update video count label
        count = len(self.wallpapers)
        self.video_count_label.set_label(f"({count})")
        
        for wp in self.wallpapers[:24]:
            card = self.create_wallpaper_card(wp)
            self.wallpaper_grid.append(card)
    
    def create_wallpaper_card(self, wallpaper):
        # Main card container
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        card.add_css_class("wallpaper-card")
        
        thumb_path = self.get_thumbnail(wallpaper['path'])
        if thumb_path and os.path.exists(thumb_path):
            try:
                # Load image naturally and scale proportionally
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(thumb_path)
                orig_w = pixbuf.get_width()
                orig_h = pixbuf.get_height()
                
                # Scale to max width 150, keep aspect ratio
                max_w = 150
                if orig_w > max_w:
                    scale = max_w / orig_w
                    new_w = max_w
                    new_h = int(orig_h * scale)
                else:
                    new_w = orig_w
                    new_h = orig_h
                
                scaled = pixbuf.scale_simple(new_w, new_h, GdkPixbuf.InterpType.BILINEAR)
                texture = Gdk.Texture.new_for_pixbuf(scaled)
                picture = Gtk.Picture.new_for_paintable(texture)
                picture.set_size_request(new_w, new_h)
                picture.add_css_class("card-thumbnail")
                card.append(picture)
            except:
                icon = Gtk.Image.new_from_icon_name("video-x-generic-symbolic")
                icon.set_pixel_size(48)
                icon.add_css_class("card-icon")
                card.append(icon)
        else:
            icon = Gtk.Image.new_from_icon_name("video-x-generic-symbolic")
            icon.set_pixel_size(48)
            icon.add_css_class("card-icon")
            card.append(icon)
        
        # Bottom row with name and delete button
        bottom_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        bottom_row.set_margin_top(4)
        bottom_row.set_margin_bottom(4)
        bottom_row.set_margin_start(4)
        bottom_row.set_margin_end(4)
        
        name = wallpaper['name'][:12] + "..." if len(wallpaper['name']) > 12 else wallpaper['name']
        name_label = Gtk.Label(label=name)
        name_label.add_css_class("card-name")
        name_label.set_ellipsize(3)
        name_label.set_hexpand(True)
        name_label.set_halign(Gtk.Align.START)
        bottom_row.append(name_label)
        
        # Delete button
        delete_btn = Gtk.Button()
        delete_btn.set_child(Gtk.Image.new_from_icon_name("user-trash-symbolic"))
        delete_btn.add_css_class("delete-btn")
        delete_btn.set_tooltip_text("Delete video")
        delete_btn.connect("clicked", self.on_delete_video, wallpaper)
        bottom_row.append(delete_btn)
        
        card.append(bottom_row)
        
        card.wallpaper_data = wallpaper
        
        return card
    
    def on_delete_video(self, button, wallpaper):
        """Remove video from local list (not from disk)"""
        dialog = Adw.MessageDialog.new(
            self,
            f"Remove '{wallpaper['name']}'?",
            "This will remove the video from the list. The file will NOT be deleted from your system."
        )
        dialog.add_response("cancel", "Cancel")
        dialog.add_response("remove", "Remove")
        dialog.set_response_appearance("remove", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_default_response("cancel")
        dialog.set_close_response("cancel")
        
        dialog.connect("response", self.on_delete_response, wallpaper)
        dialog.present()
    
    def on_delete_response(self, dialog, response, wallpaper):
        """Handle remove confirmation response"""
        if response == "remove":
            try:
                video_path = wallpaper['path']
                
                # Add to hidden videos list instead of deleting
                hidden_videos = self.config_manager.get("hidden_videos", [])
                if video_path not in hidden_videos:
                    hidden_videos.append(video_path)
                    self.config_manager.set("hidden_videos", hidden_videos)
                
                # Reload wallpapers list
                self.load_wallpapers()
            except Exception as e:
                print(f"Error removing video: {e}")

    def get_thumbnail(self, video_path):
        cache_dir = os.path.expanduser("~/.cache/snow-engine/thumbnails")
        os.makedirs(cache_dir, exist_ok=True)
        
        thumb_name = os.path.basename(video_path).replace(" ", "_") + ".jpg"
        thumb_path = os.path.join(cache_dir, thumb_name)
        
        if not os.path.exists(thumb_path):
            try:
                # Create thumbnail with 16:9 aspect ratio (320x180)
                subprocess.run([
                    "ffmpeg", "-y", "-i", video_path,
                    "-ss", "00:00:01", "-vframes", "1",
                    "-vf", "scale=320:180:force_original_aspect_ratio=increase,crop=320:180",
                    "-q:v", "2",
                    thumb_path
                ], capture_output=True, timeout=10)
            except:
                return None
        
        return thumb_path if os.path.exists(thumb_path) else None
    
    def get_youtube_video_id(self, url):
        """Extract video ID from YouTube URL"""
        import re
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})',
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def fetch_youtube_thumbnail(self, url):
        """Fetch YouTube thumbnail and display it"""
        video_id = self.get_youtube_video_id(url)
        if not video_id:
            return
        
        cache_dir = os.path.expanduser("~/.cache/snow-engine/thumbnails")
        os.makedirs(cache_dir, exist_ok=True)
        thumb_path = os.path.join(cache_dir, f"yt_{video_id}.jpg")
        
        # Try to download thumbnail
        def download_thumbnail():
            if not os.path.exists(thumb_path):
                # Try different thumbnail qualities
                thumbnail_urls = [
                    f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
                    f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
                    f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg",
                ]
                
                for thumb_url in thumbnail_urls:
                    try:
                        result = subprocess.run([
                            "curl", "-s", "-o", thumb_path, "-L", thumb_url
                        ], capture_output=True, timeout=10)
                        
                        # Check if file was downloaded and is valid
                        if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 1000:
                            break
                    except:
                        continue
            
            # Update UI in main thread
            if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 1000:
                GLib.idle_add(self.set_preview_image, thumb_path)
        
        # Run in background thread
        import threading
        thread = threading.Thread(target=download_thumbnail)
        thread.daemon = True
        thread.start()
    
    def update_preview(self):
        state = self.config_manager.load_state()
        if state and state.get("current_video"):
            video = state["current_video"]
            if state["type"] == "local":
                thumb_path = self.get_thumbnail(video)
                if thumb_path and os.path.exists(thumb_path):
                    self.set_preview_image(thumb_path)
                self.title_label.set_label(os.path.basename(video)[:20])
            elif state["type"] == "youtube":
                self.title_label.set_label("YouTube Video")
                # Try to load cached YouTube thumbnail
                video_id = self.get_youtube_video_id(video)
                if video_id:
                    cache_dir = os.path.expanduser("~/.cache/snow-engine/thumbnails")
                    thumb_path = os.path.join(cache_dir, f"yt_{video_id}.jpg")
                    if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 1000:
                        self.set_preview_image(thumb_path)
                    else:
                        self.fetch_youtube_thumbnail(video)
    
    def set_preview_image(self, image_path):
        for child in list(self.preview_image_box):
            self.preview_image_box.remove(child)
        
        if image_path and os.path.exists(image_path):
            try:
                # Load image with proper scaling - smaller for cleaner panel
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_path)
                orig_width = pixbuf.get_width()
                orig_height = pixbuf.get_height()
                
                # Scale to fit panel width (max ~180px) while keeping aspect ratio
                max_width = 180
                if orig_width > max_width:
                    scale = max_width / orig_width
                    new_width = max_width
                    new_height = int(orig_height * scale)
                else:
                    new_width = orig_width
                    new_height = orig_height
                
                # Limit height too
                max_height = 100
                if new_height > max_height:
                    scale = max_height / new_height
                    new_height = max_height
                    new_width = int(new_width * scale)
                
                scaled_pixbuf = pixbuf.scale_simple(new_width, new_height, GdkPixbuf.InterpType.BILINEAR)
                texture = Gdk.Texture.new_for_pixbuf(scaled_pixbuf)
                picture = Gtk.Picture.new_for_paintable(texture)
                picture.set_size_request(new_width, new_height)
                picture.add_css_class("preview-picture")
                self.preview_image_box.append(picture)
            except:
                pass
    
    def on_wallpaper_selected(self, flowbox, child):
        card = child.get_child()
        if hasattr(card, 'wallpaper_data'):
            wp = card.wallpaper_data
            self.selected_wallpaper = wp
            name = wp['name'][:18] + "..." if len(wp['name']) > 18 else wp['name']
            self.title_label.set_label(name)
            
            thumb_path = self.get_thumbnail(wp['path'])
            if thumb_path:
                self.set_preview_image(thumb_path)
    
    def on_apply_clicked(self, button):
        if self.selected_wallpaper:
            wp = self.selected_wallpaper
            volume = int(self.volume_slider.get_value())
            loop = self.loop_switch.get_active()
            scale_mode = self.scale_combo.get_active_id() or "fill"
            enable_audio = self.audio_switch.get_active()
            
            self.config_manager.set("volume", volume)
            self.config_manager.set("loop", loop)
            self.config_manager.set("scale_mode", scale_mode)
            self.config_manager.set("enable_audio", enable_audio)
            
            success, msg = self.mpvpaper.play(
                wp['path'],
                volume=volume,
                loop=loop,
                scale_mode=scale_mode,
                enable_audio=enable_audio
            )
            
            if success:
                self.config_manager.save_state(wp['path'], 'local')
                self.update_preview()
                self.update_status()
    
    def on_youtube_clicked(self, button):
        url = self.url_entry.get_text().strip()
        if url:
            volume = int(self.volume_slider.get_value())
            loop = self.loop_switch.get_active()
            scale_mode = self.scale_combo.get_active_id() or "fill"
            enable_audio = self.audio_switch.get_active()
            
            success, msg = self.mpvpaper.play_youtube(
                url,
                volume=volume,
                loop=loop,
                scale_mode=scale_mode,
                enable_audio=enable_audio
            )
            
            if success:
                self.config_manager.save_state(url, 'youtube')
                self.title_label.set_label("YouTube Video")
                self.update_status()
                # Fetch YouTube thumbnail
                self.fetch_youtube_thumbnail(url)
    
    def on_stop_clicked(self, button):
        self.mpvpaper.stop()
        self.update_status()
    
    def on_refresh_clicked(self, button):
        self.load_wallpapers()
    
    def on_open_folder_clicked(self, button):
        dialog = Gtk.FileDialog()
        dialog.set_title("Select Video Folder")
        dialog.select_folder(self, None, self.on_folder_selected)
    
    def on_folder_selected(self, dialog, result):
        try:
            folder = dialog.select_folder_finish(result)
            if folder:
                path = folder.get_path()
                folders = self.config_manager.get("video_folders", [])
                if path not in folders:
                    folders.append(path)
                    self.config_manager.set("video_folders", folders)
                self.load_wallpapers()
        except:
            pass
    
    def on_dark_mode_changed(self, switch, state):
        self.config_manager.set("dark_mode", state)
        self.apply_current_theme()
        return False
    
    def on_username_changed(self, entry):
        username = entry.get_text()
        self.config_manager.set("username", username)
        self.author_label.set_label(username)
    
    def on_choose_avatar(self, button):
        dialog = Gtk.FileDialog()
        dialog.set_title("Select Avatar Image")
        
        filter_images = Gtk.FileFilter()
        filter_images.set_name("Images")
        filter_images.add_mime_type("image/png")
        filter_images.add_mime_type("image/jpeg")
        filter_images.add_mime_type("image/gif")
        
        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(filter_images)
        dialog.set_filters(filters)
        
        dialog.open(self, None, self.on_avatar_selected)
    
    def on_avatar_selected(self, dialog, result):
        try:
            file = dialog.open_finish(result)
            if file:
                path = file.get_path()
                self.config_manager.set("avatar_path", path)
                self.update_avatar_display()
        except:
            pass
    
    def update_status(self):
        status = self.mpvpaper.get_status()
        
        if status.get('running'):
            self.status_label.set_label("● Running")
            self.status_label.remove_css_class("status-stopped")
            self.status_label.add_css_class("status-running")
        else:
            self.status_label.set_label("● Stopped")
            self.status_label.remove_css_class("status-running")
            self.status_label.add_css_class("status-stopped")
        
        return True


class SnowApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.snow.engine")
    
    def do_activate(self):
        win = MainWindow(self)
        win.present()


def main():
    app = SnowApp()
    app.run()


if __name__ == "__main__":
    main()
