================================================================================
                                   SynK
                        Intelligent FTP Sync Agent
                              Linux Edition
================================================================================
Original:     Anish Kalra (Roll No: 24MC3006)
              Department of Mathematical Sciences, RGIPT
Linux Port:   Ujjwal Nayan (Roll No: 24EC3041)
              Department of Electrical and Electronics Engineering, RGIPT
Release:      v1.0.0-linux
Repository:   https://github.com/Ujjwal-nayan/SynK-RGIPT-FTP-Agent
--------------------------------------------------------------------------------

1. SYSTEM REQUIREMENTS
--------------------------------------------------------------------------------
• Linux (any distribution)
  Tested on: Ubuntu 20.04+, Fedora 35+, Debian 11+, Arch Linux
• Python 3.8 or higher (pre-installed on most Linux distros)
• GTK 3 libraries (auto-installed by the installer)
• RGIPT WiFi connection

--------------------------------------------------------------------------------

2. INSTALLATION
--------------------------------------------------------------------------------
STEP 1: Extract the Archive
  $ unzip SynK-Linux.zip
  $ cd SynK-Linux

STEP 2: Run the Installer
  $ ./install.sh
  
  ⚠️  You may be prompted for your password to install GTK libraries.
      This is normal and required.

STEP 3: Launch SynK
  METHOD A: Application Menu
    • Press Super/Windows key
    • Search for "SynK"
    • Click to launch
  
  METHOD B: Terminal
    • Run: python3 ~/.local/share/synk/synk.py

--------------------------------------------------------------------------------

3. CONFIGURATION GUIDE
--------------------------------------------------------------------------------
The Setup Manager window will appear.

1. FTP Host IP: Default is 192.168.3.9.

2. Credentials: Enter your FTP User and Pass.

3. Remote Folder Name: Enter the EXACT name of the folder on the server.
   - Example: MA 221 @25-26
   - Note: This is CASE SENSITIVE. Copy the spelling exactly.

4. Save to Local Folder: Click [Browse] to pick where files go.
   - Default: ~/College Material

5. Click [+ Verify & Add Task].
   - SynK will test the connection. If it works, it adds it to the list.

6. Managing Tasks:
   - You will see your subjects in a list.
   - To remove a subject, click the Red [✕ Remove] button next to it.

7. Click [Save & Start SynK] at the bottom.

The window will close. This is normal! SynK is now running in the background.

⚠️  IMPORTANT: SynK mirrors the professor's folder exactly. If a professor
    updates a file, SynK will OVERWRITE your local copy. DO NOT save personal
    notes inside synced PDF files! Keep your notes in a separate folder.

--------------------------------------------------------------------------------

4. AUTO-START
--------------------------------------------------------------------------------
The installer automatically enables auto-start. SynK will launch silently when
you log in to your computer.

To manage auto-start manually:
  • Disable: systemctl --user disable synk.service
  • Enable:  systemctl --user enable synk.service
  • Start:   systemctl --user start synk.service
  • Stop:    systemctl --user stop synk.service
  • Status:  systemctl --user status synk.service

--------------------------------------------------------------------------------

5. TROUBLESHOOTING
--------------------------------------------------------------------------------
Q: I clicked "Save & Start" and nothing happened.
A: That means it worked. SynK is designed to run in the background invisibly.
   It will start checking for files immediately and then every 60 minutes.

Q: How do I check if SynK is running?
A: Run: systemctl --user status synk.service
   Or check logs: tail ~/.config/synk/synk.log

Q: "Connection Failed" when adding a task.
A: 1. Verify you are connected to RGIPT WiFi.
   2. Double-check username and password.
   3. Ensure the remote folder name is EXACT (case-sensitive).

Q: Files are not syncing.
A: 1. Check logs: tail ~/.config/synk/synk.log
   2. Ensure you're on RGIPT WiFi.
   3. Restart: systemctl --user restart synk.service

Q: What if a professor renames a folder?
A: Open SynK, click the Red [✕ Remove] to delete the old task, and add the
   new one with the updated folder name.

Q: SynK doesn't start automatically on login.
A: Run: systemctl --user enable synk.service
   Then log out and log back in.

Q: How do I stop it/Uninstall?
A: 1. Stop service: systemctl --user stop synk.service
   2. Disable auto-start: systemctl --user disable synk.service
   3. Remove files: rm -rf ~/.local/share/synk
   4. Remove desktop entry: rm ~/.local/share/applications/synk.desktop
   5. (Optional) Remove config: rm -rf ~/.config/synk

--------------------------------------------------------------------------------

6. TIPS FOR BEST EXPERIENCE
--------------------------------------------------------------------------------
• Organize your files in a dedicated folder:
  ~/College Material/
    ├── MA 221/      (synced by SynK)
    ├── MA 231/      (synced by SynK)
    └── My Notes/    (your personal notes - NOT synced)

• Check logs occasionally: tail ~/.config/synk/synk.log

• Multiple courses with same credentials? Just use different remote folders.

• SynK only works on RGIPT WiFi. It won't consume mobile data.

--------------------------------------------------------------------------------

SUPPORT
--------------------------------------------------------------------------------
For updates or help, visit:
Original SynK: https://github.com/Anishk362/SynK-RGIPT-FTP-Agent
Linux Port: https://github.com/Ujjwal-nayan/SynK-RGIPT-FTP-Agent

--------------------------------------------------------------------------------
                          Made with ❤️ for RGIPT Students
--------------------------------------------------------------------------------
