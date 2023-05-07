# Running Windows 'whisper'
We're going to make this all run with a mouse click by creating a shortcut.

[Back to Windows Install](INSTALL_windows.md)

[Back to Windows](FAQ_windows.md)

[Back to top](../README.md)

#### Before making the shortcut, try it in a shell to make sure it works.
```commandline
cd Documents\GitHub\fwgWhisper
python speak_write.py
```
   - Ensure there are no failures in the checks.  You will know it has passed if it pops up a file selection box
   - Select one of the test files that came with 'fwgWhisper.'  The file 'FGP_160kbps_m4a.m4a' file is a good, short choice.
   - You should see text streaming:   '<time stamp> Title, flying goat pose'
   - Let it run to confirm a text editor 'notepad' process opens with the transcribed text.   Sometimes this opens below other windows so check the taskbar for notepad processes.
   - Click in the run window 'speak_write.py' and press 'enter' when you're ready to close the run window
   - You will be copying from this type of 'notepad' window into your writing!

#### To make the shortcut do the following:
   - Browse to 'fwgWhisper.'  Click on 'speak_write.py.'  Right-click and select 'Show more options' then 'Create shortcut' down at the bottom
   - You will now see a new file 'speak_write.py - Shortcut'
   - Right-click on 'speak_write.py - Shortcut' and edit the 'Start in:' option to the place you want to store all your audio files.
   - Move the file 'speak_write.py - Shortcut' to your Desktop


[Back to Windows Install](INSTALL_windows.md)

[Back to Windows](FAQ_windows.md)

[Back to top](../README.md)
