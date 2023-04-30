# Running macOS 'whisper'
We're going to make this all run with a mouse click by creating a shortcut.

[Back to macOS INSTALL](INSTALL_macos.md)

[Back to macOS](FAQ_macos.md)

[Back to top](../README.md)

If you are not the administrator of you computer you may need to add the following to '.zprofile' or whatever startup script is needed to start your shell:

```
PATH="/Library/Frameworks/Python.framework/Versions/3.10/bin:${PATH}"
export PATH
```

Next we're going to make this all run with a mouse click by creating a shortcut.

#### Before making the shortcut, try it in a shell to make sure it works

```commandline
cd Documents/GitHub/fwgWhisper-alpha
python3.10 whisper-to-write.py
``` 
   - Ensure there are no failures in the checks.  You will know it has passed if it pops up a file selection box
   - Select one of the test files that came with 'fwgWhisper.'  The file 'FGP_160kbps_m4a.m4a' file is a good, short choice.
   - Select a model.  'tiny.en' is a good quick test.  'small.en' gives very good results for your normal use later.
   - You should see text streaming:   '<time stamp> Title, flying goat pose'
   - Let it run to confirm a text editor 'notepad' process opens with the transcribed text.   Sometimes this opens below other windows so check the taskbar for notepad processes.
   - Click in the run window 'whisper-to-write.py - Shortcut' and press 'enter' when you're ready to close the run window
   - You will be copying from this type of 'notepad' window into your writing!


#### To make the shortcut do the following:
   - Click on a script.
   - Press command-i to open the "get info" window.
   - Expand the "Open With" section (if it isn't already).
   - Choose "Python Launcher" from the drop-down menu
   - Click "Change All" if you would like ALL Python scripts to launch when double-clicked
   - Right-click again and choose 'set alias'
   - Put the resulting icon where you want it:  desktop or taskbar
   - Open a 'Terminal.'   Go to Preferences - Shell - When the shell exits'.  Select 'close if the shell exited cleanly.'  This will prevent a bunch of zombie windows from accumulating after multiple runs are completed, successfully.
   - Drag the alias to the taskbar.  It will make a copy.
   - Finally, and going forward, click on 'whisper-to-write.py alias' to test it.


[Back to macOS INSTALL](INSTALL_macos.md)

[Back to macOS](FAQ_macos.md)

[Back to top](../README.md)

