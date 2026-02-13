# Changelog - SynK Linux Port

All notable changes to the Linux port of SynK will be documented in this file.

## [1.0.0] - 2026-02-14

### Added - Initial Linux Port Release

#### Core Features
- Complete Python implementation with GTK 3 GUI
- FTP sync engine with smart file change detection (MD5 hashing)
- Multi-course support with independent credentials
- Background sync daemon with 60-minute interval
- Auto-start on login via systemd user service
- Configuration persistence in JSON format
- Comprehensive logging system

#### User Interface
- Native GTK 3 interface that respects system themes
- Clean, modern design matching Windows/macOS versions
- Real-time connection verification
- Task management (add/remove courses)
- Folder browser for selecting local directories
- Status messages and error dialogs

#### Installation & Setup
- Automated installation script (`install.sh`)
- Dependency detection and installation
- Desktop entry creation (freedesktop.org compliant)
- Systemd service setup and auto-start configuration
- Clean uninstallation script (`uninstall.sh`)

#### Documentation
- Comprehensive README.txt with full instructions
- Quick Start Guide (QUICKSTART.txt)
- Contributing guidelines (CONTRIBUTING.md)
- Inline code documentation
- Troubleshooting section

#### Linux-Specific Integration
- Systemd user service for robust background operation
- XDG Base Directory compliance (~/.config/synk/)
- Desktop file for application menu integration
- Distribution-agnostic design (works on Ubuntu, Fedora, Arch, etc.)

#### Technical Details
- Pure Python 3 implementation (no external pip dependencies)
- GTK 3 via PyGObject
- FTP using Python's ftplib
- Multi-threading for non-blocking operations
- Graceful error handling and logging

### Compatibility

#### Tested Distributions
- Ubuntu 20.04 LTS and newer
- Fedora 35 and newer
- Debian 11 and newer
- Arch Linux (rolling)

#### Requirements
- Python 3.8 or higher
- GTK 3 libraries
- RGIPT WiFi connection (192.168.3.9)

### Known Limitations

1. **Network Dependency**: Requires RGIPT WiFi to function
2. **File Overwrite**: Synced files are overwritten when professors update them (by design)
3. **No Proxy Support**: Direct FTP connection only (future enhancement)
4. **No SSL/TLS**: Uses standard FTP (matches server configuration)

### Migration from Manual Methods

Users who previously manually downloaded files from FTP can:
1. Install SynK
2. Configure their existing courses
3. Point local folders to their current download locations
4. SynK will skip files that haven't changed

### Future Enhancements (Planned)

- [ ] System tray integration
- [ ] Desktop notifications for new files
- [ ] Selective sync (filter by file extension)
- [ ] Bandwidth limiting options
- [ ] DEB/RPM package formats
- [ ] AUR package for Arch Linux
- [ ] Dark mode toggle
- [ ] Hindi localization

### Credits

**Original SynK**: Anish Kalra (24MC3006)  
**Linux Port**: Anish Kalra (24MC3006)  
**Supported by**: Dr. Chanchal Kundu, RGIPT Faculty

---

## Versioning Scheme

This project follows [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for backwards-compatible functionality additions
- PATCH version for backwards-compatible bug fixes

## Release Process

1. Update version in `synk.py`
2. Update CHANGELOG.md with changes
3. Commit changes: `git commit -am "Release vX.Y.Z"`
4. Tag release: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
5. Push: `git push && git push --tags`
6. GitHub Actions automatically creates release with binaries

---

**Note**: This changelog focuses on the Linux port. For changes to Windows/macOS versions, see the main project repository.
