#!/bin/bash

# SynK - RGIPT FTP Agent Uninstaller for Linux
# Original SynK: Anish Kalra (24MC3006)
# Linux Port: Ujjwal Nayan (24EC3041)

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           SynK Uninstallation Script                     ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Confirm uninstallation
read -p "Are you sure you want to uninstall SynK? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstallation cancelled."
    exit 0
fi

echo ""
echo "Removing SynK..."
echo ""

# Stop and disable the service
if command -v systemctl &> /dev/null; then
    echo "• Stopping background service..."
    systemctl --user stop synk.service 2>/dev/null
    systemctl --user disable synk.service 2>/dev/null
    echo "  ✓ Service stopped"
fi

# Remove systemd service file
if [ -f "$HOME/.config/systemd/user/synk.service" ]; then
    echo "• Removing systemd service..."
    rm "$HOME/.config/systemd/user/synk.service"
    systemctl --user daemon-reload 2>/dev/null
    echo "  ✓ Service file removed"
fi

# Remove desktop entry
if [ -f "$HOME/.local/share/applications/synk.desktop" ]; then
    echo "• Removing application menu entry..."
    rm "$HOME/.local/share/applications/synk.desktop"
    echo "  ✓ Desktop entry removed"
fi

# Remove installed files
if [ -d "$HOME/.local/share/synk" ]; then
    echo "• Removing program files..."
    rm -rf "$HOME/.local/share/synk"
    echo "  ✓ Program files removed"
fi

# Ask about configuration and logs
echo ""
read -p "Do you want to remove configuration and logs? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -d "$HOME/.config/synk" ]; then
        echo "• Removing configuration and logs..."
        rm -rf "$HOME/.config/synk"
        echo "  ✓ Configuration removed"
    fi
else
    echo "  ℹ Configuration and logs preserved at: ~/.config/synk/"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              ✅ Uninstallation Complete!                  ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "SynK has been removed from your system."
echo ""
echo "Thank you for using SynK! 👋"
echo ""
