# Running Windows 'whisper'
We're going to make this all run with a mouse click by creating a shortcut.

[Back to Windows Install](INSTALL_windows.md)

[Back to Windows](FAQ_windows.md)

[Back to top](../README.md)

#### Before making the shortcut, try it in a shell to make sure it works.
```commandline
cd Documents\GitHub\fwgWhisper
python GUI_Speak_Write.py
```
   - Ensure there are no failures in the checks.  You will know it has passed if it pops up a file selection box
   - Select one of the test files that came with 'fwgWhisper.'  The file 'FGP_160kbps_m4a.m4a' file is a good, short choice.
   - You should see text streaming:   '<time stamp> Title, flying goat pose'
   - Let it run to confirm a text editor 'notepad' process opens with the transcribed text.   Sometimes this opens below other windows so check the taskbar for notepad processes.
   - Click in the run window 'GUI_Speak_Write.py' and press 'enter' when you're ready to close the run window
   - You will be copying from this type of 'notepad' window into your writing!

#### To make the shortcut do the following:
   - In pyCharm run 'install.py'
   - Browse to fwgWhisper/dist/gui_speak_write to find 'gui_speak_write.exe'.  Right-click on it to  make shortcut.
   - Right click on shortcut to 'pin to taskbar'


[Back to Windows Install](INSTALL_windows.md)

[Back to Windows](FAQ_windows.md)

[Back to top](../README.md)
