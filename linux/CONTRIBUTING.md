# Contributing to SynK - Linux Port

Thank you for your interest in contributing to SynK! This document provides guidelines for contributing to the Linux port of SynK.

## Linux Port Development

This Linux port was created to bring SynK's functionality to Linux users at RGIPT. The goal is to maintain feature parity with Windows and macOS versions while providing native Linux integration.

## How to Contribute

### Reporting Bugs

If you find a bug in the Linux version:

1. Check if the bug has already been reported in [Issues](https://github.com/Anishk362/SynK-RGIPT-FTP-Agent/issues)
2. If not, create a new issue with:
   - Your Linux distribution and version
   - Python version (`python3 --version`)
   - Steps to reproduce the bug
   - Expected vs actual behavior
   - Relevant logs from `~/.config/synk/synk.log`

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:

1. Check existing issues to avoid duplicates
2. Clearly describe the enhancement
3. Explain why it would be useful
4. Consider if it maintains cross-platform consistency

### Pull Requests

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test on multiple Linux distributions if possible
5. Update documentation (README.txt) if needed
6. Commit with clear messages: `git commit -m "Add: feature description"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Development Setup

### Prerequisites

```bash
# Ubuntu/Debian
sudo apt install python3 python3-gi python3-gi-cairo gir1.2-gtk-3.0

# Fedora/RHEL
sudo dnf install python3 python3-gobject gtk3

# Arch
sudo pacman -S python python-gobject gtk3
```

### Running from Source

```bash
cd SynK-Linux
python3 synk.py
```

### Testing Daemon Mode

```bash
python3 synk.py --daemon
```

## Code Style Guidelines

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and modular
- Use type hints where appropriate

## Testing

Test your changes on:
- Ubuntu 22.04 LTS (or newer)
- Fedora (latest stable)
- Arch Linux (if possible)

Verify:
- GUI launches correctly
- Tasks can be added/removed
- FTP connection works
- Background sync functions
- Auto-start works
- Logs are written correctly

## Documentation

When adding features:
- Update README.txt with usage instructions
- Add comments in code
- Update CONTRIBUTING.md if process changes

## Areas for Contribution

Potential areas where contributions are welcome:

1. **Distribution-Specific Packages**
   - DEB package for Debian/Ubuntu
   - RPM package for Fedora/RHEL
   - AUR package for Arch Linux

2. **UI Enhancements**
   - System tray integration
   - Desktop notifications for new files
   - Dark mode support

3. **Features**
   - Multiple FTP server support
   - Selective file sync (filter by extension)
   - Bandwidth limiting
   - Proxy support

4. **Testing**
   - Unit tests
   - Integration tests
   - CI/CD pipeline

5. **Documentation**
   - Video tutorials
   - Screenshots
   - Translation to Hindi

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn
- Remember this is built for students, by students

## Questions?

Contact: Anish Kalra (24MC3006@rgipt.ac.in)

## License

By contributing, you agree that your contributions will be licensed under the same terms as the original SynK project.

---

**Thank you for making SynK better for all RGIPT students!** 🚀
