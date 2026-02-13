#!/bin/bash

# SynK - RGIPT FTP Agent Installer for Linux
# Original SynK: Anish Kalra (24MC3006)
# Linux Port: Ujjwal Nayan (24EC3041)

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║       SynK - RGIPT FTP Agent Installation Script          ║"
echo "║              Linux Port by Ujjwal Nayan                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Error: This script is for Linux only!"
    exit 1
fi

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed!"
    echo "   Please install Python 3 using your package manager:"
    echo "   - Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "   - Fedora/RHEL:   sudo dnf install python3 python3-pip"
    echo "   - Arch:          sudo pacman -S python python-pip"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check for GTK
if ! python3 -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk" &> /dev/null; then
    echo ""
    echo "⚠️  GTK 3 not found. Installing required dependencies..."
    echo ""
    
    # Detect package manager
    if command -v apt &> /dev/null; then
        echo "   Installing via apt..."
        sudo apt update
        sudo apt install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0
    elif command -v dnf &> /dev/null; then
        echo "   Installing via dnf..."
        sudo dnf install -y python3-gobject gtk3
    elif command -v pacman &> /dev/null; then
        echo "   Installing via pacman..."
        sudo pacman -S --noconfirm python-gobject gtk3
    else
        echo "❌ Error: Could not detect package manager!"
        echo "   Please manually install: python3-gi and gtk3"
        exit 1
    fi
fi

echo "✓ GTK 3 libraries found"
echo ""

# Create installation directory
INSTALL_DIR="$HOME/.local/share/synk"
mkdir -p "$INSTALL_DIR"

echo "📦 Installing SynK..."

# Copy main application
cp synk.py "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/synk.py"

# Create desktop entry
DESKTOP_FILE="$HOME/.local/share/applications/synk.desktop"
mkdir -p "$HOME/.local/share/applications"

cat > "$DESKTOP_FILE" << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=SynK
Comment=RGIPT FTP Agent - Automatic Course Material Sync
Exec=python3 %HOME%/.local/share/synk/synk.py
Icon=folder-download
Terminal=false
Categories=Network;Education;
Keywords=ftp;sync;rgipt;education;
EOF

# Replace %HOME% with actual home directory
sed -i "s|%HOME%|$HOME|g" "$DESKTOP_FILE"

echo "✓ Desktop entry created"

# Create systemd user service for auto-start
SYSTEMD_DIR="$HOME/.config/systemd/user"
mkdir -p "$SYSTEMD_DIR"

cat > "$SYSTEMD_DIR/synk.service" << EOF
[Unit]
Description=SynK - RGIPT FTP Agent Background Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $INSTALL_DIR/synk.py --daemon
Restart=on-failure
RestartSec=60
Environment="DISPLAY=:0"

[Install]
WantedBy=default.target
EOF

echo "✓ Systemd service created"

# Enable systemd service
if command -v systemctl &> /dev/null; then
    systemctl --user daemon-reload
    systemctl --user enable synk.service
    echo "✓ Auto-start enabled (will start on next login)"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              ✅ Installation Complete!                    ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 To launch SynK:"
echo "   - Search for 'SynK' in your application menu, OR"
echo "   - Run: python3 ~/.local/share/synk/synk.py"
echo ""
echo "📝 Configuration files are stored in: ~/.config/synk/"
echo "📋 Logs are stored in: ~/.config/synk/synk.log"
echo ""
echo "⚡ The background service will start automatically on your next login."
echo "   To start it now, run: systemctl --user start synk.service"
echo ""
echo "For updates or help, visit:"
echo "  Original SynK: https://github.com/Anishk362/SynK-RGIPT-FTP-Agent"
echo "  Linux Port:    https://github.com/Ujjwal-nayan/SynK-RGIPT-FTP-Agent"
echo ""
