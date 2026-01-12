import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk

LIGHT_CSS = """
window {
    background: linear-gradient(135deg, #e8d5f2 0%, #d4e5f7 50%, #f0e6f5 100%);
}

.main-container {
    background: rgba(255, 255, 255, 0.88);
    border-radius: 18px;
    border: 1px solid rgba(255, 255, 255, 0.95);
}

.sidebar {
    background: transparent;
    padding: 10px 8px;
    min-width: 130px;
}


.snow-logo {
    font-size: 32px;
    color: #a855f7;
    text-shadow: 0 2px 6px rgba(168, 85, 247, 0.4);
    margin-bottom: 2px;
}

.snow-title {
    font-size: 14px;
    font-weight: 700;
    color: #1e293b;
    letter-spacing: 1px;
}

.snow-subtitle {
    font-size: 10px;
    font-weight: 500;
    color: #64748b;
    letter-spacing: 1px;
}

.sidebar-header {
    padding: 14px 8px;
    margin-bottom: 10px;
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(236, 72, 153, 0.1) 100%);
    border-radius: 14px;
    border: 1px solid rgba(168, 85, 247, 0.2);
}


.monitor-icon {
    background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
    border-radius: 10px;
    padding: 8px;
    min-width: 36px;
    min-height: 36px;
}

.monitor-label {
    font-size: 12px;
    font-weight: 600;
    color: #1e293b;
}

.menu-label {
    font-size: 9px;
    font-weight: 500;
    color: #64748b;
    padding: 4px 6px;
}

.menu-item {
    background: transparent;
    border: none;
    border-radius: 10px;
    padding: 10px 14px;
    margin: 3px 0;
}

.menu-item:hover {
    background: rgba(168, 85, 247, 0.12);
}

.menu-item.active {
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.2) 0%, rgba(236, 72, 153, 0.12) 100%);
    border-left: 3px solid #a855f7;
}

.menu-item label {
    font-size: 13px;
    font-weight: 500;
    color: #475569;
}

.menu-item:hover label, .menu-item.active label {
    color: #7c3aed;
}

.menu-icon {
    color: #94a3b8;
    min-width: 16px;
}

.menu-item:hover .menu-icon, .menu-item.active .menu-icon {
    color: #7c3aed;
}

.content-area {
    background: transparent;
    padding: 14px;
}

.feeds-header {
    padding: 4px 0 10px 0;
}

.feeds-title {
    font-size: 18px;
    font-weight: 700;
    color: #1e293b;
}

.video-count {
    font-size: 13px;
    font-weight: 500;
    color: #a855f7;
    background: rgba(168, 85, 247, 0.12);
    padding: 2px 10px;
    border-radius: 12px;
}

.tab-button {
    background: transparent;
    border: none;
    padding: 5px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
    color: #94a3b8;
}

.tab-button:hover { color: #7c3aed; }
.tab-button.active { color: #7c3aed; font-weight: 600; }

.wallpaper-grid {
    padding: 8px;
}

.wallpaper-card {
    background: #ffffff;
    border-radius: 10px;
    border: 2px solid transparent;
    padding: 4px;
}

.wallpaper-card:hover {
    box-shadow: 0 4px 16px rgba(168, 85, 247, 0.25);
    border-color: #a855f7;
}

.card-thumbnail {
    border-radius: 8px;
}

.card-icon {
    color: #a855f7;
    padding: 20px;
}

.card-name {
    font-size: 10px;
    font-weight: 500;
    color: #334155;
}

.delete-btn {
    background: rgba(239, 68, 68, 0.1);
    border: none;
    border-radius: 6px;
    padding: 4px;
    min-width: 24px;
    min-height: 24px;
    opacity: 0.6;
}

.delete-btn:hover {
    background: rgba(239, 68, 68, 0.25);
    opacity: 1;
}

.delete-btn image {
    color: #ef4444;
}

flowboxchild {
    padding: 4px;
    margin: 0;
    border-radius: 12px;
    color: #ffffff;
    font-size: 16px;
}

flowboxchild {
    padding: 4px;
    margin: 0;
    border-radius: 12px;
}

flowboxchild:selected {
    background: rgba(168, 85, 247, 0.15);
    border-radius: 12px;
}

flowboxchild:selected .wallpaper-card {
    border-color: #a855f7;
}

.right-panel {
    background: rgba(255, 255, 255, 0.98);
    border-radius: 16px;
    padding: 14px;
    min-width: 220px;
    margin: 4px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(168, 85, 247, 0.1);
}

.search-entry {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 7px 14px;
    font-size: 12px;
    color: #64748b;
}

.search-entry:focus {
    border-color: #a855f7;
    box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.1);
}

.icon-button {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid #e2e8f0;
    border-radius: 50%;
    padding: 8px;
    min-width: 34px;
    min-height: 34px;
}

.icon-button:hover {
    background: #ffffff;
    border-color: #a855f7;
}

.icon-button.primary {
    background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
    border: none;
    color: #ffffff;
}

.preview-card {
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    margin-bottom: 10px;
}

.preview-image {
    border-radius: 12px;
    background: transparent;
}

.preview-picture {
    border-radius: 12px;
}

.preview-title {
    font-size: 14px;
    font-weight: 600;
    color: #1e293b;
    padding: 8px;
}

.stars { color: #fbbf24; font-size: 13px; }

.subscribe-button {
    background: linear-gradient(135deg, #f472b6 0%, #ec4899 100%);
    border: none;
    border-radius: 16px;
    padding: 7px 20px;
    color: #ffffff;
    font-size: 12px;
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(236, 72, 153, 0.25);
}

.subscribe-button:hover {
    box-shadow: 0 4px 14px rgba(236, 72, 153, 0.35);
}

.control-label {
    font-size: 11px;
    font-weight: 500;
    color: #64748b;
}

.control-slider trough {
    background: #e2e8f0;
    border-radius: 6px;
    min-height: 4px;
}

.control-slider highlight {
    background: linear-gradient(90deg, #a855f7, #ec4899);
    border-radius: 6px;
}

.control-slider slider {
    background: #ffffff;
    border: 2px solid #a855f7;
    border-radius: 50%;
    min-width: 12px;
    min-height: 12px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

/* Compact Footer Styles */
.panel-footer {
    background: rgba(248, 250, 252, 0.95);
    border-radius: 10px;
    padding: 8px 12px;
    border: 1px solid rgba(226, 232, 240, 0.8);
}

.mini-avatar {
    background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
    border-radius: 50%;
    min-width: 24px;
    min-height: 24px;
    padding: 0;
    border: none;
}

.mini-avatar picture {
    border-radius: 50%;
    min-width: 24px;
    min-height: 24px;
}

.mini-avatar-image {
    border-radius: 50%;
}

.mini-snow-icon {
    font-size: 12px;
    color: #ffffff;
}

.footer-name {
    font-size: 12px;
    font-weight: 600;
    color: #475569;
}

.mini-stop-button {
    background: rgba(244, 114, 182, 0.15);
    border: 1px solid rgba(244, 114, 182, 0.3);
    border-radius: 6px;
    padding: 4px 10px;
    color: #ec4899;
    font-size: 10px;
    font-weight: 600;
}

.mini-stop-button:hover {
    background: rgba(244, 114, 182, 0.25);
}

.footer-brand {
    font-size: 12px;
    font-weight: 600;
    color: #7c3aed;
}

.apply-btn {
    background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
    border: none;
    border-radius: 8px;
    padding: 4px 12px;
    color: #ffffff;
    font-size: 11px;
    font-weight: 600;
}

.apply-btn:hover {
    box-shadow: 0 2px 8px rgba(168, 85, 247, 0.35);
}

.preview-card {
    background: rgba(255, 255, 255, 0.6);
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 10px;
}

.preview-title {
    font-size: 12px;
    font-weight: 600;
    color: #475569;
}

.preview-picture {
    border-radius: 8px;
}

.author-section {
    padding: 0;
    border: none;
    margin: 0;
}

.status-stopped {
    font-size: 10px;
    color: #94a3b8;
}

.status-playing {
    font-size: 10px;
    color: #10b981;
}

.avatar-picture {
    border-radius: 50%;
    min-width: 32px;
    min-height: 32px;
}

.preview-picture {
    border-radius: 10px;
    min-width: 180px;
    min-height: 100px;
}

.preview-image {
    border-radius: 10px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100px;
}

.preview-image picture {
    border-radius: 10px;
}

.author-name {
    font-size: 11px;
    font-weight: 600;
    color: #1e293b;
}

.app-branding {
    font-size: 12px;
    font-weight: 600;
    color: #1e293b;
    padding: 10px;
}

switch:checked {
    background: linear-gradient(90deg, #a855f7, #ec4899);
}

.play-button {
    background: linear-gradient(135deg, #a855f7 0%, #7c3aed 100%);
    border: none;
    border-radius: 6px;
    padding: 6px 14px;
    color: #ffffff;
    font-size: 11px;
    font-weight: 600;
    box-shadow: 0 2px 6px rgba(124, 58, 237, 0.25);
}

.stop-button {
    background: linear-gradient(135deg, #f472b6 0%, #ec4899 100%);
    border: none;
    border-radius: 6px;
    padding: 6px 14px;
    color: #ffffff;
    font-size: 11px;
    font-weight: 600;
}

.url-entry {
    background: #ffffff;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 12px;
    color: #1e293b;
}

.url-entry:focus {
    border-color: #a855f7;
}

.status-running { color: #10b981; font-weight: 600; }
.status-stopped { color: #ef4444; font-weight: 600; }

.scale-dropdown {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 11px;
}

.settings-section {
    background: rgba(255, 255, 255, 0.6);
    border-radius: 10px;
    padding: 12px;
    margin: 6px 0;
}

.settings-title {
    font-size: 13px;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 8px;
}

.spin-entry {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 4px 8px;
    font-size: 11px;
    min-width: 70px;
}

.refresh-button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    border: none;
    border-radius: 8px;
    padding: 6px 12px;
    color: #ffffff;
    font-size: 11px;
    font-weight: 600;
}

.folder-button {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    border: none;
    border-radius: 8px;
    padding: 6px 12px;
    color: #ffffff;
    font-size: 11px;
    font-weight: 600;
}
"""

DARK_CSS = """
window {
    background: linear-gradient(135deg, #1a1625 0%, #1e1b2e 50%, #252136 100%);
}

.main-container {
    background: rgba(30, 27, 46, 0.92);
    border-radius: 18px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.sidebar {
    background: transparent;
    padding: 10px 8px;
    min-width: 130px;
}


.snow-logo {
    font-size: 32px;
    color: #a855f7;
    text-shadow: 0 2px 6px rgba(168, 85, 247, 0.4);
    margin-bottom: 2px;
}

.snow-title {
    font-size: 14px;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: 1px;
}

.snow-subtitle {
    font-size: 10px;
    font-weight: 500;
    color: #a855f7;
    letter-spacing: 1px;
}

.sidebar-header {
    padding: 14px 8px;
    margin-bottom: 10px;
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.2) 0%, rgba(236, 72, 153, 0.15) 100%);
    border-radius: 14px;
    border: 1px solid rgba(168, 85, 247, 0.25);
}


.monitor-icon {
    background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
    border-radius: 10px;
    padding: 8px;
    min-width: 36px;
    min-height: 36px;
}

.monitor-label {
    font-size: 12px;
    font-weight: 600;
    color: #e2e8f0;
}

.menu-label {
    font-size: 9px;
    font-weight: 500;
    color: #94a3b8;
    padding: 4px 6px;
}

.menu-item {
    background: transparent;
    border: none;
    border-radius: 10px;
    padding: 10px 14px;
    margin: 3px 0;
    transition: all 0.2s ease;
}

.menu-item:hover {
    background: rgba(168, 85, 247, 0.2);
}

.menu-item.active {
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.3) 0%, rgba(236, 72, 153, 0.2) 100%);
    border-left: 3px solid #a855f7;
}

.menu-item label {
    font-size: 13px;
    font-weight: 500;
    color: #cbd5e1;
}

.menu-item:hover label, .menu-item.active label {
    color: #e9d5ff;
}

.menu-icon {
    color: #8b5cf6;
    min-width: 18px;
}

.menu-item:hover .menu-icon, .menu-item.active .menu-icon {
    color: #c084fc;
}

.content-area {
    background: transparent;
    padding: 18px;
}

.feeds-header {
    padding: 6px 0 14px 0;
}

.feeds-title {
    font-size: 18px;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: 0.5px;
}

.video-count {
    font-size: 13px;
    font-weight: 500;
    color: #c084fc;
    background: rgba(168, 85, 247, 0.2);
    padding: 2px 10px;
    border-radius: 12px;
}

.tab-button {
    background: transparent;
    border: none;
    padding: 5px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
    color: #64748b;
}

.tab-button:hover { color: #c084fc; }
.tab-button.active { color: #c084fc; font-weight: 600; }

.wallpaper-grid {
    padding: 8px;
}

.wallpaper-card {
    background: rgba(45, 40, 65, 0.95);
    border-radius: 10px;
    border: 2px solid transparent;
    padding: 4px;
}

.wallpaper-card:hover {
    box-shadow: 0 4px 16px rgba(168, 85, 247, 0.5);
    border-color: #a855f7;
}

.card-thumbnail {
    border-radius: 8px;
}

.card-icon {
    color: #a855f7;
    padding: 20px;
}

.card-name {
    font-size: 10px;
    font-weight: 500;
    color: #e2e8f0;
}

.delete-btn {
    background: rgba(239, 68, 68, 0.15);
    border: none;
    border-radius: 6px;
    padding: 4px;
    min-width: 24px;
    min-height: 24px;
    opacity: 0.6;
}

.delete-btn:hover {
    background: rgba(239, 68, 68, 0.35);
    opacity: 1;
}

.delete-btn image {
    color: #f87171;
}

flowboxchild {
    padding: 4px;
    margin: 0;
    border-radius: 12px;
}

flowboxchild:selected {
    background: rgba(168, 85, 247, 0.2);
    border-radius: 12px;
}

flowboxchild:selected .wallpaper-card {
    border-color: #a855f7;
    box-shadow: 0 6px 20px rgba(168, 85, 247, 0.4);
}

.right-panel {
    background: rgba(30, 27, 50, 0.95);
    border-radius: 14px;
    padding: 12px;
    min-width: 200px;
    margin: 4px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.icon-button {
    background: rgba(45, 40, 65, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 50%;
    padding: 6px;
    min-width: 28px;
    min-height: 28px;
}

.icon-button:hover {
    border-color: #a855f7;
}

.icon-button.primary {
    background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
    border: none;
}

.preview-card {
    background: transparent;
    margin-bottom: 8px;
}

.preview-image {
    border-radius: 10px;
    background: transparent;
}

.preview-picture {
    border-radius: 10px;
}

.preview-title {
    font-size: 13px;
    font-weight: 600;
    color: #f1f5f9;
    padding: 6px 0;
}

.stars { 
    color: #fbbf24; 
    font-size: 12px;
    letter-spacing: 1px;
}

.subscribe-button {
    background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
    border: none;
    border-radius: 16px;
    padding: 8px 24px;
    color: #ffffff;
    font-size: 12px;
    font-weight: 600;
}

.subscribe-button:hover {
    opacity: 0.9;
}

.control-label {
    font-size: 11px;
    font-weight: 500;
    color: #94a3b8;
}

.control-slider trough {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    min-height: 4px;
}

.control-slider highlight {
    background: linear-gradient(90deg, #a855f7, #ec4899);
    border-radius: 8px;
}

.control-slider slider {
    background: #f1f5f9;
    border: 2px solid #a855f7;
    border-radius: 50%;
    min-width: 16px;
    min-height: 16px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

/* Compact Footer Styles */
.panel-footer {
    background: rgba(45, 40, 65, 0.6);
    border-radius: 10px;
    padding: 8px 12px;
    border: 1px solid rgba(168, 85, 247, 0.15);
}

.mini-avatar {
    background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
    border-radius: 50%;
    min-width: 24px;
    min-height: 24px;
    padding: 0;
    border: none;
}

.mini-avatar picture {
    border-radius: 50%;
    min-width: 24px;
    min-height: 24px;
}

.mini-avatar-image {
    border-radius: 50%;
}

.mini-snow-icon {
    font-size: 12px;
    color: #ffffff;
}

.footer-name {
    font-size: 12px;
    font-weight: 600;
    color: #e2e8f0;
}

.mini-stop-button {
    background: rgba(244, 114, 182, 0.2);
    border: 1px solid rgba(244, 114, 182, 0.35);
    border-radius: 6px;
    padding: 4px 10px;
    color: #f472b6;
    font-size: 10px;
    font-weight: 600;
}

.mini-stop-button:hover {
    background: rgba(244, 114, 182, 0.35);
}

.footer-brand {
    font-size: 12px;
    font-weight: 600;
    color: #c4b5fd;
}

.apply-btn {
    background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
    border: none;
    border-radius: 8px;
    padding: 4px 12px;
    color: #ffffff;
    font-size: 11px;
    font-weight: 600;
}

.apply-btn:hover {
    box-shadow: 0 2px 8px rgba(168, 85, 247, 0.4);
}

.preview-card {
    background: rgba(45, 40, 65, 0.4);
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 10px;
}

.preview-title {
    font-size: 12px;
    font-weight: 600;
    color: #e2e8f0;
}

.preview-picture {
    border-radius: 8px;
}

.status-running { 
    color: #34d399; 
    font-size: 10px;
    font-weight: 500;
}

.status-stopped { 
    color: #94a3b8; 
    font-size: 10px;
    font-weight: 500;
}

.status-playing { 
    color: #34d399; 
    font-size: 10px;
    font-weight: 500;
}

.preview-picture {
    border-radius: 10px;
}

.preview-image {
    border-radius: 10px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100px;
}

.preview-image picture {
    border-radius: 10px;
}

.author-name {
    font-size: 13px;
    font-weight: 600;
    color: #f1f5f9;
}

.app-branding {
    font-size: 13px;
    font-weight: 700;
    color: #c084fc;
    padding: 12px;
    letter-spacing: 0.5px;
}

switch {
    background: #3d3656;
    border-radius: 14px;
    min-width: 48px;
    min-height: 26px;
}

switch:checked {
    background: linear-gradient(90deg, #a855f7, #ec4899);
}

switch slider {
    border-radius: 50%;
    min-width: 22px;
    min-height: 22px;
    background: #ffffff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.play-button {
    background: linear-gradient(135deg, #a855f7 0%, #7c3aed 100%);
    border: none;
    border-radius: 8px;
    padding: 8px 14px;
    color: #ffffff;
    font-size: 11px;
    font-weight: 600;
}

.play-button:hover {
    opacity: 0.9;
}

.url-entry {
    background: rgba(45, 40, 65, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 11px;
    color: #f1f5f9;
}

.url-entry:focus {
    border-color: #a855f7;
}

.status-running { 
    color: #34d399; 
    font-weight: 600;
    font-size: 13px;
}
.status-stopped { 
    color: #f87171; 
    font-weight: 600;
    font-size: 13px;
}

.scale-dropdown {
    background: rgba(45, 40, 65, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 10px;
    padding: 8px 12px;
    font-size: 12px;
    color: #cbd5e1;
}

.scale-dropdown:hover {
    border-color: #a855f7;
}

.settings-section {
    background: rgba(45, 40, 65, 0.6);
    border-radius: 14px;
    padding: 16px;
    margin: 8px 0;
    border: 1px solid rgba(168, 85, 247, 0.1);
}

.settings-title {
    font-size: 14px;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 12px;
    letter-spacing: 0.5px;
}

.spin-entry {
    background: rgba(45, 40, 65, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 12px;
    color: #f1f5f9;
    min-width: 80px;
}

.refresh-button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    border: none;
    border-radius: 10px;
    padding: 8px 16px;
    color: #ffffff;
    font-size: 12px;
    font-weight: 600;
    box-shadow: 0 4px 10px rgba(16, 185, 129, 0.35);
    transition: all 0.2s ease;
}

.refresh-button:hover {
    box-shadow: 0 6px 16px rgba(16, 185, 129, 0.45);
}

.folder-button {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    border: none;
    border-radius: 10px;
    padding: 8px 16px;
    color: #ffffff;
    font-size: 12px;
    font-weight: 600;
    box-shadow: 0 4px 10px rgba(59, 130, 246, 0.35);
    transition: all 0.2s ease;
}

.folder-button:hover {
    box-shadow: 0 6px 16px rgba(59, 130, 246, 0.45);
}
"""

def apply_theme(dark_mode=False):
    css_provider = Gtk.CssProvider()
    css_provider.load_from_string(DARK_CSS if dark_mode else LIGHT_CSS)
    
    display = Gdk.Display.get_default()
    Gtk.StyleContext.add_provider_for_display(
        display,
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
    return css_provider
