╔═══════════════════════════════════════════════════════════════════╗
║                   SynK v1.0.0 - Linux Edition                     ║
║          Intelligent FTP Agent for RGIPT Students                 ║
╚═══════════════════════════════════════════════════════════════════╝

Author: Anish Kalra (Roll No: 24MC3006)
Department of Mathematical Sciences, RGIPT
Linux Port Contribution

═══════════════════════════════════════════════════════════════════

📖 WHAT IS SynK?
═══════════════════════════════════════════════════════════════════

SynK is a "Set it and Forget it" background utility designed exclusively
for RGIPT students on Linux. It connects to the college Intranet FTP,
monitors your specific subject folders (e.g., "MA 221 @25-26"), and
automatically downloads new slides, assignments, and PDFs to your laptop
the moment they are uploaded by professors.

🌟 KEY FEATURES:
  ✓ Zero Distraction: Runs silently in the background
  ✓ Intranet Only: Works on RGIPT WiFi without internet/Cyberoam login
  ✓ Smart Sync: Checks every 60 minutes, updates changed files only
  ✓ Multi-Course: Handle all your subjects in one place
  ✓ Auto-Start: Launches automatically when you log in

═══════════════════════════════════════════════════════════════════

💾 SYSTEM REQUIREMENTS
═══════════════════════════════════════════════════════════════════

• Operating System: Linux (any distribution)
  - Tested on: Ubuntu 20.04+, Fedora 35+, Arch Linux, Debian 11+
  
• Software Requirements:
  - Python 3.8 or higher (pre-installed on most Linux distros)
  - GTK 3 libraries (will be installed automatically if missing)
  
• Network: RGIPT WiFi connection

═══════════════════════════════════════════════════════════════════

📦 INSTALLATION INSTRUCTIONS
═══════════════════════════════════════════════════════════════════

STEP 1: Extract the Archive
─────────────────────────────────────────────────────────────────
Extract the downloaded SynK-Linux.zip file to a temporary location:

  $ unzip SynK-Linux.zip
  $ cd SynK-Linux

STEP 2: Run the Installer
─────────────────────────────────────────────────────────────────
Run the installation script (it will automatically install dependencies):

  $ ./install.sh

⚠️  You may be prompted for your password to install system dependencies
    (GTK libraries). This is normal and required.

STEP 3: Launch SynK
─────────────────────────────────────────────────────────────────
After installation, you can launch SynK in two ways:

  METHOD A: Application Menu
  • Press Super/Windows key
  • Search for "SynK"
  • Click to launch

  METHOD B: Terminal
  • Run: python3 ~/.local/share/synk/synk.py

═══════════════════════════════════════════════════════════════════

⚙️  CONFIGURATION GUIDE
═══════════════════════════════════════════════════════════════════

Once SynK opens, you'll see a clean interface to add your courses.

ADDING A SUBJECT:
─────────────────────────────────────────────────────────────────
1. FTP Host: Leave as default (192.168.3.9)

2. Username: Your FTP username (provided by your professor)

3. Password: Your FTP password

4. Remote Folder: The EXACT folder name from the FTP server
   ⚠️  CRITICAL: This is CASE SENSITIVE!
   
   Examples:
   ✓ Correct: "MA 221 @25-26"
   ✗ Wrong:   "ma 221 @25-26"
   ✗ Wrong:   "MA221@25-26"
   
   Copy the folder name EXACTLY as it appears on the FTP server.

5. Local Folder: Where you want the files saved on your computer
   • Default: ~/College Material
   • Click "Browse" to choose a different location
   
   ⚠️  IMPORTANT: SynK mirrors the professor's folder exactly.
       If a professor updates a file, SynK will OVERWRITE your local copy.
       DO NOT save personal notes inside the synced PDF files!
       Keep your notes in a separate folder.

6. Click "+ Verify & Add Task"
   • SynK will test the connection
   • Wait for the "Success" message
   • Your subject will appear in the "Current Tasks" list below

MANAGING TASKS:
─────────────────────────────────────────────────────────────────
• To remove a subject: Click the red "✕ Remove" button next to it
• To add another subject: Fill in the form again and click "+ Verify & Add Task"

STARTING SynK:
─────────────────────────────────────────────────────────────────
• Once you've added all your subjects, click "Save & Start SynK"
• The window will close/minimize
• SynK is now running in the background!

═══════════════════════════════════════════════════════════════════

🔧 ADVANCED FEATURES
═══════════════════════════════════════════════════════════════════

AUTO-START ON LOGIN:
─────────────────────────────────────────────────────────────────
The installer automatically enables auto-start. SynK will launch
silently when you log in to your computer.

To manage auto-start manually:
  • Disable: systemctl --user disable synk.service
  • Enable:  systemctl --user enable synk.service
  • Start:   systemctl --user start synk.service
  • Stop:    systemctl --user stop synk.service
  • Status:  systemctl --user status synk.service

VIEW LOGS:
─────────────────────────────────────────────────────────────────
Check what SynK is doing:

  $ tail -f ~/.config/synk/synk.log

This shows real-time sync activity, including:
  • When SynK starts/stops
  • Files being synchronized
  • Any errors encountered

CONFIGURATION FILE:
─────────────────────────────────────────────────────────────────
Your tasks are stored in JSON format at:
  ~/.config/synk/config.json

You can edit this file manually if needed (advanced users only).

═══════════════════════════════════════════════════════════════════

❓ TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════

PROBLEM: "Connection Failed" when adding a task
─────────────────────────────────────────────────────────────────
SOLUTION:
  1. Verify you are connected to "RGIPT WiFi"
  2. Double-check username and password
  3. Ensure the remote folder name is EXACT (case-sensitive)
  4. Try accessing the FTP manually using FileZilla to verify credentials

PROBLEM: SynK doesn't start automatically on login
─────────────────────────────────────────────────────────────────
SOLUTION:
  1. Run: systemctl --user enable synk.service
  2. Log out and log back in
  3. Check status: systemctl --user status synk.service

PROBLEM: Files not syncing
─────────────────────────────────────────────────────────────────
SOLUTION:
  1. Check logs: tail ~/.config/synk/synk.log
  2. Ensure you're on RGIPT WiFi
  3. Verify the remote folder still exists (professor may have renamed it)
  4. Restart SynK: systemctl --user restart synk.service

PROBLEM: Professor renamed a folder
─────────────────────────────────────────────────────────────────
SOLUTION:
  1. Open SynK
  2. Click the red "✕ Remove" button for the old task
  3. Add a new task with the new folder name

PROBLEM: Want to stop SynK temporarily
─────────────────────────────────────────────────────────────────
SOLUTION:
  Terminal: systemctl --user stop synk.service
  (To restart: systemctl --user start synk.service)

═══════════════════════════════════════════════════════════════════

🗑️  UNINSTALLATION
═══════════════════════════════════════════════════════════════════

To completely remove SynK from your system:

  1. Stop the background service:
     $ systemctl --user stop synk.service
     $ systemctl --user disable synk.service

  2. Remove installed files:
     $ rm -rf ~/.local/share/synk
     $ rm ~/.local/share/applications/synk.desktop
     $ rm ~/.config/systemd/user/synk.service

  3. (Optional) Remove configuration and logs:
     $ rm -rf ~/.config/synk

═══════════════════════════════════════════════════════════════════

📊 DIFFERENCES FROM WINDOWS/macOS VERSIONS
═══════════════════════════════════════════════════════════════════

The Linux version of SynK maintains feature parity with Windows and
macOS versions while providing native Linux integration:

SIMILARITIES:
  ✓ Same core FTP sync engine
  ✓ Same 60-minute sync interval
  ✓ Same smart file change detection
  ✓ Same multi-course support
  ✓ Same user interface design

LINUX-SPECIFIC FEATURES:
  + Systemd integration for robust background service
  + GTK 3 native interface (respects your system theme)
  + freedesktop.org compliant desktop entry
  + Better process management and logging
  + Works with any Linux distribution

═══════════════════════════════════════════════════════════════════

💡 TIPS FOR BEST EXPERIENCE
═══════════════════════════════════════════════════════════════════

1. ORGANIZE YOUR FILES
   Create a dedicated folder structure like:
   ~/College Material/
     ├── MA 221/          (synced by SynK)
     ├── MA 231/          (synced by SynK)
     └── My Notes/        (your personal notes - NOT synced)

2. BACKUP IMPORTANT WORK
   Since SynK overwrites files when professors update them, never
   save important personal work inside synced folders.

3. MULTIPLE COURSES, SAME CREDENTIALS
   If all your professors use the same FTP username/password, you
   can still add multiple tasks - just use different remote folders.

4. CHECK LOGS OCCASIONALLY
   Run: tail ~/.config/synk/synk.log
   This helps you know if SynK is working properly.

5. STAY ON RGIPT WIFI
   SynK only works when connected to RGIPT WiFi. It won't consume
   your mobile data or work from home.

═══════════════════════════════════════════════════════════════════

🤝 CONTRIBUTING & FEEDBACK
═══════════════════════════════════════════════════════════════════

This Linux port was created as a contribution to make SynK available
to all RGIPT students regardless of their operating system choice.

Found a bug? Have a suggestion? Want to contribute?
Contact: Anish Kalra (24MC3006@rgipt.ac.in)

GitHub: https://github.com/Anishk362/SynK-RGIPT-FTP-Agent

═══════════════════════════════════════════════════════════════════

📄 LICENSE & CREDITS
═══════════════════════════════════════════════════════════════════

SynK - RGIPT FTP Agent
Original Version: Anish Kalra (24MC3006)
Linux Port: Anish Kalra (24MC3006)

Developed for students of:
Rajiv Gandhi Institute of Petroleum Technology (RGIPT)
Amethi, Uttar Pradesh, India

This software is provided free of charge for educational purposes.

═══════════════════════════════════════════════════════════════════

🎓 ACKNOWLEDGMENTS
═══════════════════════════════════════════════════════════════════

Special thanks to:
• Dr. Chanchal Kundu - For supporting and promoting SynK
• All RGIPT faculty members who maintain the FTP server
• RGIPT students for testing and feedback

═══════════════════════════════════════════════════════════════════

                  Happy Syncing! 🚀
                Made with ❤️  for RGIPT Students

═══════════════════════════════════════════════════════════════════
