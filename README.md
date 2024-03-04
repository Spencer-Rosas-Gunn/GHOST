# GHOST
Qt5-Based Minimalist Web Browser

This is a reupload from my old GitHub account. You can find the original [here](https://github.com/Sig-Moid/GHOST/blob/main/ghost.py), but it's no longer being maintained (since I lost the login to that account). The README is hereafter a one-for-one copy of that README. Please forgive the bad writing as such, since this is half a year old and I've learned a lot since then.

### What is GHOST?

The GHOST (Guardian Hypertext Online Secure Transmitter) project, or Guardian Browser for short, is a Qt5-based web browser that sends standard HTTPS/HTTP requests for ASCII HTML files via Qt5Transmit and reads them with the Qt5HTML/CSS reader widget. GHOST provides high-security JavaScript support, as well as protection against fingerprinting (especially with WebGL). It provides a simple, minimalist interface with tilde-based commands.

### How can I use it?

GHOST has three commands, notated by tildes (~dark, ~lite, ~inst N) that switch the graphical mode (~dark/~lite) or switch the current "instance" (~inst N). Instances are integer IDs (0 - 999) that store cookies and can be switched between seamlessly. All cookies in an instance can be tracelessly deleted by merely clicking the instance counter. Dark/Light mode preferences are consistent tab-to-tab, but are not remembered between sessions. The only data GHOST stores between sessions is cookie data, which is 100% deleted whenever the instance holding said cookies is deleted.

### What does it support?

GHOST supports JavaScript 4.0. GHOST has the infrastructure to support WebGL & WASM, but the former has a fingerprinting exploitation that, until resolved, has prevented it's use in release versions. We are currently working on a solution to mask hardware information to prevent WebGL fingerprinting.

### How do I install it?

Download Python3 from https://www.python.org/downloads/, then run the terminal commands "pip install PyQt5" & "pip install cookiejar" in "IDLE" (the first application in the Python3 folder). With the setup done, download the browser itself from GitHub (https://github.com/Sig-Moid/GHOST) by downloading the "ghost.py" file. Set the file to open with Python Launcher (the second application in the Python3 folder) by default. If you aren't on MacOS, you're done! Simply double click the file whenever you want to use it. If you are on MacOS, try to open the file. If it fails with the message "this file is broken and can't be opened, you should move it to the trash" (or something similar), go to your terminal and type the command "xattr -d com.apple.quarantine " before dragging your file into the terminal window and pressing enter. Now the file should work.
