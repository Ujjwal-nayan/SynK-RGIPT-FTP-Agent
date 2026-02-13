# 🐧 SynK - Linux Port

<div align="center">

![Downloads](https://img.shields.io/github/downloads/Anishk362/SynK-RGIPT-FTP-Agent/total?style=for-the-badge&color=2ea44f&label=TOTAL%20DOWNLOADS)
![Version](https://img.shields.io/github/v/release/Anishk362/SynK-RGIPT-FTP-Agent?style=for-the-badge&color=blue)
![License](https://img.shields.io/badge/License-Educational-orange?style=for-the-badge)

**Intelligent FTP Agent for RGIPT Students**

*Stop manually checking for course updates. Let SynK do it for you.*

[Download Latest Release](https://github.com/Anishk362/SynK-RGIPT-FTP-Agent/releases/latest) • [Report Bug](https://github.com/Anishk362/SynK-RGIPT-FTP-Agent/issues) • [Request Feature](https://github.com/Anishk362/SynK-RGIPT-FTP-Agent/issues)

</div>

---

## 📖 About

SynK is a "Set it and Forget it" background utility designed exclusively for RGIPT students on Linux. It connects to the college Intranet FTP, monitors your specific subject folders (e.g., `MA 221 @25-26`), and automatically downloads new slides, assignments, and PDFs to your laptop the moment they are uploaded by professors.

### ✨ Key Features

- 🎯 **Zero Distraction**: Runs silently in the background with no open windows
- 🔒 **Intranet Only**: Works strictly on RGIPT WiFi without consuming internet data
- 🧠 **Smart Sync**: Checks every 60 minutes, only downloads changed files
- 📚 **Multi-Course**: Handle all your subjects in one place
- 🚀 **Auto-Start**: Launches automatically when you log in
- 🐧 **Native Linux**: GTK 3 interface, systemd integration, respects your desktop theme

---

## 🎬 Quick Demo

```bash
# Extract and install
$ unzip SynK-Linux.zip
$ cd SynK-Linux
$ ./install.sh

# Launch SynK
$ python3 ~/.local/share/synk/synk.py

# Or search for "SynK" in your application menu
```

---

## 💾 System Requirements

| Requirement | Details |
|------------|---------|
| **OS** | Any Linux distribution |
| **Python** | 3.8 or higher (usually pre-installed) |
| **Libraries** | GTK 3 (auto-installed by installer) |
| **Network** | RGIPT WiFi connection |

### Tested Distributions

- ✅ Ubuntu 20.04, 22.04, 24.04
- ✅ Fedora 35, 36, 37, 38
- ✅ Debian 11, 12
- ✅ Arch Linux (rolling)
- ✅ Linux Mint 20, 21

---

## 📦 Installation

### Method 1: Automated Installer (Recommended)

1. **Download** the latest release:
   ```bash
   wget https://github.com/Anishk362/SynK-RGIPT-FTP-Agent/releases/latest/download/SynK-Linux.zip
   ```

2. **Extract** the archive:
   ```bash
   unzip SynK-Linux.zip
   cd SynK-Linux
   ```

3. **Run** the installer:
   ```bash
   ./install.sh
   ```
   > The installer will automatically detect your distribution and install dependencies

4. **Launch** SynK:
   - Search for "SynK" in your application menu, OR
   - Run: `python3 ~/.local/share/synk/synk.py`

### Method 2: Manual Installation

If you prefer manual installation:

```bash
# Install dependencies (choose your distro)

# Ubuntu/Debian
sudo apt install python3 python3-gi python3-gi-cairo gir1.2-gtk-3.0

# Fedora/RHEL
sudo dnf install python3 python3-gobject gtk3

# Arch
sudo pacman -S python python-gobject gtk3

# Copy files
mkdir -p ~/.local/share/synk
cp synk.py ~/.local/share/synk/
chmod +x ~/.local/share/synk/synk.py

# Create desktop entry
mkdir -p ~/.local/share/applications
cat > ~/.local/share/applications/synk.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=SynK
Comment=RGIPT FTP Agent
Exec=python3 $HOME/.local/share/synk/synk.py
Icon=folder-download
Terminal=false
Categories=Network;Education;
EOF
```

---

## ⚙️ Configuration

### Adding Your First Course

1. **Launch SynK** from your application menu
2. **Fill in the details**:
   - **FTP Host**: `192.168.3.9` (leave default)
   - **Username**: Your FTP username (from professor)
   - **Password**: Your FTP password
   - **Remote Folder**: `MA 221 @25-26` ⚠️ **CASE SENSITIVE!**
   - **Local Folder**: `~/College Material` (or browse to choose)
3. **Click**: `+ Verify & Add Task`
4. **Wait** for the "Success" message
5. **Click**: `Save & Start SynK`

### Adding Multiple Courses

Simply repeat the process for each subject. SynK handles multiple FTP credentials seamlessly.

### Managing Courses

- **Remove a course**: Click the red `✕ Remove` button
- **Change local folder**: Remove and re-add with new path
- **Update credentials**: Remove and re-add with new credentials

---

## 🔧 Advanced Usage

### Auto-Start Management

SynK automatically starts on login via systemd. To manage:

```bash
# Disable auto-start
systemctl --user disable synk.service

# Enable auto-start
systemctl --user enable synk.service

# Start immediately
systemctl --user start synk.service

# Stop running instance
systemctl --user stop synk.service

# Check status
systemctl --user status synk.service
```

### View Real-Time Logs

```bash
# Follow logs live
tail -f ~/.config/synk/synk.log

# View last 50 lines
tail -n 50 ~/.config/synk/synk.log
```

### Configuration File

Tasks are stored in JSON at `~/.config/synk/config.json`:

```json
{
  "tasks": [
    {
      "host": "192.168.3.9",
      "port": 21,
      "username": "your_username",
      "password": "your_password",
      "remote_folder": "MA 221 @25-26",
      "local_folder": "/home/you/College Material/MA 221"
    }
  ]
}
```

### Daemon Mode

Run SynK in pure daemon mode (no GUI):

```bash
python3 ~/.local/share/synk/synk.py --daemon
```

---

## ❓ Troubleshooting

<details>
<summary><b>Connection Failed</b> when adding a task</summary>

**Solutions**:
1. Verify you're on RGIPT WiFi
2. Double-check username and password
3. Ensure remote folder name is EXACT (case-sensitive)
4. Test with FileZilla first to verify credentials
</details>

<details>
<summary>SynK <b>doesn't auto-start</b> on login</summary>

**Solutions**:
```bash
systemctl --user enable synk.service
systemctl --user start synk.service
```
Log out and log back in.
</details>

<details>
<summary><b>Files not syncing</b></summary>

**Solutions**:
1. Check logs: `tail ~/.config/synk/synk.log`
2. Ensure you're on RGIPT WiFi
3. Verify remote folder still exists (professor may have renamed it)
4. Restart: `systemctl --user restart synk.service`
</details>

<details>
<summary>Professor <b>renamed a folder</b></summary>

**Solution**:
1. Open SynK
2. Remove the old task (✕ button)
3. Add new task with updated folder name
</details>

<details>
<summary><b>GTK import error</b></summary>

**Solution**: Install GTK libraries for your distribution:
```bash
# Ubuntu/Debian
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0

# Fedora
sudo dnf install python3-gobject gtk3

# Arch
sudo pacman -S python-gobject gtk3
```
</details>

---

## 🗑️ Uninstallation

```bash
cd SynK-Linux
./uninstall.sh
```

Or manually:

```bash
systemctl --user stop synk.service
systemctl --user disable synk.service
rm -rf ~/.local/share/synk
rm ~/.local/share/applications/synk.desktop
rm ~/.config/systemd/user/synk.service
rm -rf ~/.config/synk  # Optional: removes config and logs
```

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### Areas for Contribution

- 📦 Distribution-specific packages (DEB, RPM, AUR)
- 🎨 UI enhancements (system tray, notifications)
- ✨ New features (selective sync, bandwidth limiting)
- 🧪 Testing and bug reports
- 📚 Documentation improvements

---

## 📊 Project Status

![Issues](https://img.shields.io/github/issues/Anishk362/SynK-RGIPT-FTP-Agent?style=flat-square)
![Pull Requests](https://img.shields.io/github/issues-pr/Anishk362/SynK-RGIPT-FTP-Agent?style=flat-square)
![Last Commit](https://img.shields.io/github/last-commit/Anishk362/SynK-RGIPT-FTP-Agent?style=flat-square)

---

## 📄 License

This software is provided free of charge for educational purposes at RGIPT.

---

## 👨‍💻 Author

**Anish Kalra**  
Roll No: 24MC3006  
Department of Mathematical Sciences  
Rajiv Gandhi Institute of Petroleum Technology (RGIPT)  
Email: 24MC3006@rgipt.ac.in

---

## 🙏 Acknowledgments

- **Dr. Chanchal Kundu** - For supporting and promoting SynK
- **RGIPT Faculty** - For maintaining the FTP infrastructure
- **RGIPT Students** - For testing and feedback
- **Open Source Community** - For GTK and Python

---

## 📸 Screenshots

### Main Interface
![SynK Main Window](https://via.placeholder.com/800x600?text=SynK+Main+Window)

### Task Management
![Task List](https://via.placeholder.com/800x400?text=Task+Management)

---

## 🔗 Links

- [Main Project](https://github.com/Anishk362/SynK-RGIPT-FTP-Agent)
- [Windows Version](https://github.com/Anishk362/SynK-RGIPT-FTP-Agent/releases/latest)
- [macOS Version](https://github.com/Anishk362/SynK-RGIPT-FTP-Agent/releases/latest)
- [Report Issues](https://github.com/Anishk362/SynK-RGIPT-FTP-Agent/issues)

---

<div align="center">

**Made with ❤️ for RGIPT Students**

⭐ Star this repo if SynK helps you! ⭐

</div>
