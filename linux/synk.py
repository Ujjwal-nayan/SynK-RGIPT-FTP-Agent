#!/usr/bin/env python3
"""
SynK - Intelligent FTP Agent for RGIPT (Linux Port)
Automatically syncs course materials from RGIPT Intranet FTP

Original SynK: Anish Kalra (24MC3006)
Linux Port: Ujjwal Nayan (24EC3041)
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk
import json
import os
import sys
from pathlib import Path
from ftplib import FTP, error_perm
import threading
import time
from datetime import datetime
import hashlib

# Configuration paths
CONFIG_DIR = Path.home() / '.config' / 'synk'
CONFIG_FILE = CONFIG_DIR / 'config.json'
LOG_FILE = CONFIG_DIR / 'synk.log'

# Ensure config directory exists
CONFIG_DIR.mkdir(parents=True, exist_ok=True)


class SynKConfig:
    """Handles configuration management"""
    
    def __init__(self):
        self.tasks = []
        self.load()
    
    def load(self):
        """Load configuration from file"""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', [])
            except Exception as e:
                self.log(f"Error loading config: {e}")
    
    def save(self):
        """Save configuration to file"""
        try:
            data = {'tasks': self.tasks}
            with open(CONFIG_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            self.log(f"Error saving config: {e}")
            return False
    
    def add_task(self, task):
        """Add a new sync task"""
        self.tasks.append(task)
        return self.save()
    
    def remove_task(self, index):
        """Remove a sync task"""
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            return self.save()
        return False
    
    @staticmethod
    def log(message):
        """Log message to file"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")


class FTPSyncEngine:
    """Handles FTP synchronization logic"""
    
    def __init__(self, config):
        self.config = config
        self.running = False
        self.sync_thread = None
    
    def verify_connection(self, host, port, username, password, remote_folder):
        """Test FTP connection and folder access"""
        try:
            ftp = FTP()
            ftp.connect(host, port, timeout=10)
            ftp.login(username, password)
            
            # Try to change to remote folder
            ftp.cwd(remote_folder)
            
            ftp.quit()
            return True, "Connection successful!"
        except error_perm as e:
            return False, f"Permission denied or folder not found: {e}"
        except Exception as e:
            return False, f"Connection failed: {e}"
    
    def get_file_hash(self, filepath):
        """Calculate MD5 hash of a file"""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return None
    
    def sync_folder(self, task):
        """Sync a single folder from FTP (including subdirectories)"""
        try:
            host = task.get('host', '192.168.3.9')
            port = task.get('port', 21)
            username = task['username']
            password = task['password']
            remote_folder = task['remote_folder']
            local_folder = Path(task['local_folder'])
            
            # Create local folder if it doesn't exist
            local_folder.mkdir(parents=True, exist_ok=True)
            
            # Connect to FTP
            ftp = FTP()
            ftp.connect(host, port, timeout=30)
            ftp.login(username, password)
            
            synced_count = self._sync_directory_recursive(ftp, remote_folder, local_folder)
            
            ftp.quit()
            
            if synced_count > 0:
                SynKConfig.log(f"Synced {synced_count} file(s) from {remote_folder}")
            
            return True
            
        except Exception as e:
            SynKConfig.log(f"Error in sync_folder for {task.get('remote_folder', 'unknown')}: {e}")
            return False
    
    def _sync_directory_recursive(self, ftp, remote_path, local_path):
        """Recursively sync a directory and all its subdirectories"""
        synced_count = 0
        
        try:
            # Change to the remote directory
            ftp.cwd(remote_path)
            
            # Get directory listing with details
            items = []
            ftp.retrlines('LIST', items.append)
            
            for item in items:
                # Parse LIST output (Unix-style: drwxr-xr-x or -rw-r--r--)
                parts = item.split(None, 8)
                if len(parts) < 9:
                    continue
                
                permissions = parts[0]
                name = parts[8]
                
                # Skip . and .. directories
                if name in ['.', '..']:
                    continue
                
                # Check if it's a directory (starts with 'd')
                if permissions.startswith('d'):
                    # It's a directory - recurse into it
                    new_local_path = local_path / name
                    new_local_path.mkdir(parents=True, exist_ok=True)
                    
                    # Recursively sync subdirectory
                    synced_count += self._sync_directory_recursive(
                        ftp, 
                        f"{remote_path}/{name}", 
                        new_local_path
                    )
                    
                    # Change back to parent directory
                    ftp.cwd(remote_path)
                else:
                    # It's a file - download it
                    try:
                        local_file = local_path / name
                        temp_file = local_path / f".{name}.tmp"
                        
                        # Download to temp file first
                        with open(temp_file, 'wb') as f:
                            ftp.retrbinary(f'RETR {name}', f.write)
                        
                        # Check if file changed
                        if local_file.exists():
                            old_hash = self.get_file_hash(local_file)
                            new_hash = self.get_file_hash(temp_file)
                            
                            if old_hash == new_hash:
                                # File unchanged, remove temp
                                temp_file.unlink()
                                continue
                        
                        # Move temp file to actual location
                        temp_file.replace(local_file)
                        synced_count += 1
                        SynKConfig.log(f"Synced: {name} to {local_path}")
                        
                    except Exception as e:
                        SynKConfig.log(f"Error syncing file {name}: {e}")
                        if temp_file.exists():
                            temp_file.unlink()
            
            return synced_count
            
        except Exception as e:
            SynKConfig.log(f"Error in _sync_directory_recursive for {remote_path}: {e}")
            return synced_count
    
    def sync_all_tasks(self):
        """Sync all configured tasks"""
        for task in self.config.tasks:
            if self.running:
                self.sync_folder(task)
    
    def start_sync_loop(self):
        """Start the background sync loop"""
        self.running = True
        
        def sync_worker():
            SynKConfig.log("SynK background service started")
            while self.running:
                try:
                    self.sync_all_tasks()
                    # Sleep for 60 minutes (3600 seconds)
                    for _ in range(360):  # Check every 10 seconds if we should stop
                        if not self.running:
                            break
                        time.sleep(10)
                except Exception as e:
                    SynKConfig.log(f"Error in sync loop: {e}")
                    time.sleep(60)
            
            SynKConfig.log("SynK background service stopped")
        
        self.sync_thread = threading.Thread(target=sync_worker, daemon=True)
        self.sync_thread.start()
    
    def stop_sync_loop(self):
        """Stop the background sync loop"""
        self.running = False


class SynKGUI(Gtk.Window):
    """Main GUI window for SynK"""
    
    def __init__(self):
        super().__init__(title="SynK - RGIPT FTP Agent")
        self.set_default_size(700, 600)
        self.set_border_width(10)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # Load CSS for styling
        self.load_css()
        
        self.config = SynKConfig()
        self.engine = FTPSyncEngine(self.config)
        
        self.setup_ui()
        
        # Connect close event
        self.connect("delete-event", self.on_close)
    
    def load_css(self):
        """Load custom CSS styling"""
        css_provider = Gtk.CssProvider()
        css = b"""
        .header-label {
            font-size: 18px;
            font-weight: bold;
            color: #2ea44f;
        }
        .task-box {
            background-color: #f6f8fa;
            border-radius: 6px;
            padding: 10px;
        }
        .primary-button {
            background-color: #2ea44f;
            color: white;
            font-weight: bold;
            border-radius: 6px;
            padding: 10px;
        }
        .danger-button {
            background-color: #d73a49;
            color: white;
            border-radius: 4px;
        }
        """
        css_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def setup_ui(self):
        """Setup the user interface"""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.add(main_box)
        
        # Header
        header = Gtk.Label()
        header.set_markup("<span size='x-large' weight='bold' foreground='#2ea44f'>🚀 SynK: Intelligent FTP Agent for RGIPT</span>")
        main_box.pack_start(header, False, False, 0)
        
        # Subtitle
        subtitle = Gtk.Label()
        subtitle.set_markup("<i>Stop manually checking for course updates. Let SynK do it for you.</i>")
        main_box.pack_start(subtitle, False, False, 0)
        
        # Separator
        main_box.pack_start(Gtk.Separator(), False, False, 5)
        
        # Add Task Section
        add_frame = Gtk.Frame(label=" Add New Subject ")
        add_frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        add_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        add_box.set_border_width(10)
        add_frame.add(add_box)
        
        # FTP Host
        host_box = Gtk.Box(spacing=10)
        host_box.pack_start(Gtk.Label("FTP Host:", xalign=0, width_chars=15), False, False, 0)
        self.host_entry = Gtk.Entry()
        self.host_entry.set_text("192.168.3.9")
        self.host_entry.set_placeholder_text("Default: 192.168.3.9")
        host_box.pack_start(self.host_entry, True, True, 0)
        add_box.pack_start(host_box, False, False, 0)
        
        # Username
        user_box = Gtk.Box(spacing=10)
        user_box.pack_start(Gtk.Label("Username:", xalign=0, width_chars=15), False, False, 0)
        self.username_entry = Gtk.Entry()
        self.username_entry.set_placeholder_text("FTP Username")
        user_box.pack_start(self.username_entry, True, True, 0)
        add_box.pack_start(user_box, False, False, 0)
        
        # Password
        pass_box = Gtk.Box(spacing=10)
        pass_box.pack_start(Gtk.Label("Password:", xalign=0, width_chars=15), False, False, 0)
        self.password_entry = Gtk.Entry()
        self.password_entry.set_visibility(False)
        self.password_entry.set_placeholder_text("FTP Password")
        pass_box.pack_start(self.password_entry, True, True, 0)
        add_box.pack_start(pass_box, False, False, 0)
        
        # Remote Folder
        remote_box = Gtk.Box(spacing=10)
        remote_box.pack_start(Gtk.Label("Remote Folder:", xalign=0, width_chars=15), False, False, 0)
        self.remote_entry = Gtk.Entry()
        self.remote_entry.set_placeholder_text("e.g., MA 221 @25-26 (Case Sensitive!)")
        remote_box.pack_start(self.remote_entry, True, True, 0)
        add_box.pack_start(remote_box, False, False, 0)
        
        # Local Folder
        local_box = Gtk.Box(spacing=10)
        local_box.pack_start(Gtk.Label("Local Folder:", xalign=0, width_chars=15), False, False, 0)
        self.local_entry = Gtk.Entry()
        self.local_entry.set_text(str(Path.home() / "College Material"))
        local_box.pack_start(self.local_entry, True, True, 0)
        browse_btn = Gtk.Button(label="Browse")
        browse_btn.connect("clicked", self.on_browse_folder)
        local_box.pack_start(browse_btn, False, False, 0)
        add_box.pack_start(local_box, False, False, 0)
        
        # Add Task Button
        add_btn = Gtk.Button(label="+ Verify & Add Task")
        add_btn.get_style_context().add_class("primary-button")
        add_btn.connect("clicked", self.on_add_task)
        add_box.pack_start(add_btn, False, False, 5)
        
        main_box.pack_start(add_frame, False, False, 0)
        
        # Current Tasks Section
        tasks_frame = Gtk.Frame(label=" Current Tasks ")
        tasks_frame.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        
        # Scrolled window for tasks
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_height(200)
        
        self.tasks_list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.tasks_list_box.set_border_width(10)
        scrolled.add(self.tasks_list_box)
        tasks_frame.add(scrolled)
        
        main_box.pack_start(tasks_frame, True, True, 0)
        
        # Bottom Buttons
        button_box = Gtk.Box(spacing=10)
        button_box.set_homogeneous(True)
        
        self.save_start_btn = Gtk.Button(label="Save & Start SynK")
        self.save_start_btn.get_style_context().add_class("primary-button")
        self.save_start_btn.connect("clicked", self.on_save_and_start)
        button_box.pack_start(self.save_start_btn, True, True, 0)
        
        main_box.pack_start(button_box, False, False, 0)
        
        # Refresh task list
        self.refresh_tasks_list()
    
    def on_browse_folder(self, widget):
        """Open folder chooser dialog"""
        dialog = Gtk.FileChooserDialog(
            title="Select Local Sync Folder",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.local_entry.set_text(dialog.get_filename())
        
        dialog.destroy()
    
    def on_add_task(self, widget):
        """Add a new sync task after verification"""
        host = self.host_entry.get_text().strip()
        username = self.username_entry.get_text().strip()
        password = self.password_entry.get_text().strip()
        remote_folder = self.remote_entry.get_text().strip()
        local_folder = self.local_entry.get_text().strip()
        
        # Validation
        if not all([username, password, remote_folder, local_folder]):
            self.show_message("Error", "Please fill in all fields!", Gtk.MessageType.ERROR)
            return
        
        # Show verification dialog
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.NONE,
            text="Verifying Connection..."
        )
        dialog.format_secondary_text("Please wait while we verify the FTP connection...")
        dialog.show_all()
        
        def verify_thread():
            success, message = self.engine.verify_connection(
                host, 21, username, password, remote_folder
            )
            
            GLib.idle_add(dialog.destroy)
            
            if success:
                task = {
                    'host': host,
                    'port': 21,
                    'username': username,
                    'password': password,
                    'remote_folder': remote_folder,
                    'local_folder': local_folder
                }
                
                if self.config.add_task(task):
                    GLib.idle_add(self.show_message, "Success", 
                                "Task added successfully!", Gtk.MessageType.INFO)
                    GLib.idle_add(self.refresh_tasks_list)
                    GLib.idle_add(self.clear_form)
                else:
                    GLib.idle_add(self.show_message, "Error", 
                                "Failed to save task!", Gtk.MessageType.ERROR)
            else:
                GLib.idle_add(self.show_message, "Connection Failed", message, 
                            Gtk.MessageType.ERROR)
        
        thread = threading.Thread(target=verify_thread, daemon=True)
        thread.start()
    
    def clear_form(self):
        """Clear the add task form"""
        self.username_entry.set_text("")
        self.password_entry.set_text("")
        self.remote_entry.set_text("")
    
    def refresh_tasks_list(self):
        """Refresh the list of current tasks"""
        # Clear existing widgets
        for child in self.tasks_list_box.get_children():
            self.tasks_list_box.remove(child)
        
        if not self.config.tasks:
            label = Gtk.Label()
            label.set_markup("<i>No tasks configured yet. Add a subject above to get started!</i>")
            self.tasks_list_box.pack_start(label, False, False, 10)
        else:
            for idx, task in enumerate(self.config.tasks):
                task_box = Gtk.Box(spacing=10)
                task_box.get_style_context().add_class("task-box")
                task_box.set_border_width(5)
                
                # Task info
                info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
                
                title_label = Gtk.Label(xalign=0)
                title_label.set_markup(f"<b>{task['remote_folder']}</b>")
                info_box.pack_start(title_label, False, False, 0)
                
                path_label = Gtk.Label(xalign=0)
                path_label.set_markup(f"<small>→ {task['local_folder']}</small>")
                info_box.pack_start(path_label, False, False, 0)
                
                task_box.pack_start(info_box, True, True, 0)
                
                # Delete button
                delete_btn = Gtk.Button(label="✕ Remove")
                delete_btn.get_style_context().add_class("danger-button")
                delete_btn.connect("clicked", self.on_remove_task, idx)
                task_box.pack_start(delete_btn, False, False, 0)
                
                self.tasks_list_box.pack_start(task_box, False, False, 0)
        
        self.tasks_list_box.show_all()
    
    def on_remove_task(self, widget, index):
        """Remove a sync task"""
        if self.config.remove_task(index):
            self.refresh_tasks_list()
            self.show_message("Success", "Task removed!", Gtk.MessageType.INFO)
    
    def on_save_and_start(self, widget):
        """Save config and start background sync"""
        if not self.config.tasks:
            self.show_message("No Tasks", "Please add at least one task before starting SynK!", 
                            Gtk.MessageType.WARNING)
            return
        
        # Start the sync engine
        self.engine.start_sync_loop()
        
        # Minimize to system (hide window)
        self.hide()
        
        # Show notification
        self.show_message("SynK Started", 
                         "SynK is now running in the background!\n\n" +
                         "It will check for updates every 60 minutes.\n" +
                         "To stop SynK, close this application from the system menu.",
                         Gtk.MessageType.INFO)
    
    def show_message(self, title, message, message_type):
        """Show a message dialog"""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=message_type,
            buttons=Gtk.ButtonsType.OK,
            text=title
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()
    
    def on_close(self, widget, event):
        """Handle window close event"""
        if self.engine.running:
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text="Stop SynK?"
            )
            dialog.format_secondary_text(
                "SynK is currently running in the background.\n" +
                "Do you want to stop it?"
            )
            
            response = dialog.run()
            dialog.destroy()
            
            if response == Gtk.ResponseType.YES:
                self.engine.stop_sync_loop()
                Gtk.main_quit()
                return False
            else:
                # Just hide the window, keep running
                self.hide()
                return True
        else:
            Gtk.main_quit()
            return False


def daemon_mode():
    """Run in daemon mode (background only, no GUI)"""
    SynKConfig.log("SynK daemon mode started")
    
    config = SynKConfig()
    if not config.tasks:
        SynKConfig.log("No tasks configured. Exiting daemon mode.")
        return
    
    engine = FTPSyncEngine(config)
    engine.start_sync_loop()
    
    # Keep the daemon running
    try:
        while engine.running:
            time.sleep(1)
    except KeyboardInterrupt:
        SynKConfig.log("Daemon interrupted by user")
        engine.stop_sync_loop()


def main():
    """Main entry point"""
    # Check for daemon mode
    if '--daemon' in sys.argv or '-d' in sys.argv:
        daemon_mode()
        return
    
    # Check if we're on RGIPT WiFi
    import socket
    try:
        # Try to resolve the FTP server
        socket.gethostbyname('192.168.3.9')
    except:
        print("⚠️  Warning: Cannot reach RGIPT FTP server (192.168.3.9)")
        print("    Please ensure you are connected to RGIPT WiFi")
        print()
    
    app = SynKGUI()
    app.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
