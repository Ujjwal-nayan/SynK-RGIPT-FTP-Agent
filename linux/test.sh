#!/bin/bash

# SynK Linux Port - Test Suite
# Original SynK: Anish Kalra (24MC3006)
# Linux Port: Ujjwal Nayan

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              SynK Linux Port - Test Suite                ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((TESTS_PASSED++))
}

fail() {
    echo -e "${RED}✗${NC} $1"
    ((TESTS_FAILED++))
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Test 1: Python version
echo "Testing Python installation..."
if python3 --version &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    if [[ $(echo "$PYTHON_VERSION" | cut -d'.' -f1) -ge 3 ]] && [[ $(echo "$PYTHON_VERSION" | cut -d'.' -f2) -ge 8 ]]; then
        pass "Python $PYTHON_VERSION is installed"
    else
        fail "Python version $PYTHON_VERSION is too old (need 3.8+)"
    fi
else
    fail "Python 3 is not installed"
fi

# Test 2: GTK libraries
echo ""
echo "Testing GTK libraries..."
if python3 -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk" &> /dev/null; then
    GTK_VERSION=$(python3 -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk; print(f'{Gtk.MAJOR_VERSION}.{Gtk.MINOR_VERSION}.{Gtk.MICRO_VERSION}')")
    pass "GTK $GTK_VERSION is available"
else
    fail "GTK 3 libraries are not installed"
fi

# Test 3: File structure
echo ""
echo "Testing file structure..."
FILES=("synk.py" "install.sh" "uninstall.sh" "README.txt" "QUICKSTART.txt")
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        pass "Found $file"
    else
        fail "Missing $file"
    fi
done

# Test 4: Script permissions
echo ""
echo "Testing script permissions..."
for script in "install.sh" "uninstall.sh" "synk.py"; do
    if [ -x "$script" ]; then
        pass "$script is executable"
    else
        warn "$script is not executable (run: chmod +x $script)"
    fi
done

# Test 5: Python syntax
echo ""
echo "Testing Python syntax..."
if python3 -m py_compile synk.py 2>/dev/null; then
    pass "synk.py has valid Python syntax"
else
    fail "synk.py has syntax errors"
fi

# Test 6: Import dependencies
echo ""
echo "Testing Python imports..."
IMPORTS=("json" "os" "sys" "pathlib" "ftplib" "threading" "time" "datetime" "hashlib")
for module in "${IMPORTS[@]}"; do
    if python3 -c "import $module" &> /dev/null; then
        pass "Can import $module"
    else
        fail "Cannot import $module"
    fi
done

# Test 7: Configuration directory
echo ""
echo "Testing configuration setup..."
CONFIG_DIR="$HOME/.config/synk-test"
mkdir -p "$CONFIG_DIR"
if [ -d "$CONFIG_DIR" ]; then
    pass "Configuration directory can be created"
    rm -rf "$CONFIG_DIR"
else
    fail "Cannot create configuration directory"
fi

# Test 8: FTP connectivity (if on RGIPT WiFi)
echo ""
echo "Testing network connectivity..."
if ping -c 1 -W 2 192.168.3.9 &> /dev/null; then
    pass "Can reach RGIPT FTP server (192.168.3.9)"
    warn "Note: This test only checks ping, not FTP access"
else
    warn "Cannot reach RGIPT FTP server (not on RGIPT WiFi or server down)"
fi

# Test 9: Systemd availability
echo ""
echo "Testing systemd..."
if command -v systemctl &> /dev/null; then
    pass "systemctl is available"
    if systemctl --user show-environment &> /dev/null; then
        pass "User systemd services are supported"
    else
        warn "User systemd services may not be fully supported"
    fi
else
    warn "systemctl not found (auto-start won't work)"
fi

# Test 10: Desktop file validation
echo ""
echo "Testing desktop entry..."
if command -v desktop-file-validate &> /dev/null; then
    # Create a temporary desktop file for testing
    cat > /tmp/synk-test.desktop << EOF
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
    
    if desktop-file-validate /tmp/synk-test.desktop &> /dev/null; then
        pass "Desktop file format is valid"
    else
        fail "Desktop file has validation errors"
    fi
    rm /tmp/synk-test.desktop
else
    warn "desktop-file-validate not found (can't validate .desktop file)"
fi

# Summary
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                      Test Summary                         ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "Tests Passed: $TESTS_PASSED"
echo "Tests Failed: $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed! ✓${NC}"
    echo "The system is ready for SynK installation."
    exit 0
else
    echo -e "${RED}Some tests failed! ✗${NC}"
    echo "Please resolve the issues before installing SynK."
    exit 1
fi
