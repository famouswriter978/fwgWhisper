# Running Linux 'whisper'
We're going to make this all run with a mouse click by creating a shortcut.

[Back to Linux INSTALL](INSTALL_linux.md)

[Back to Linux](FAQ_linux.md)

[Back to top](../README.md)

#### Before making the shortcut, try it in a shell to make sure it works.
``` commandline
cd Documents/GitHub/fwgWhisper
python3 speak_write.py
```
   - Ensure there are no failures in the checks.  You will know it has passed if it pops up a file selection box
   - Select one of the test files that came with 'fwgWhisper.'  The file 'FGP_160kbps_m4a.m4a' file is a good, short choice.
   - Select a model.  'tiny.en' is a good quick test.  'small.en' gives very good results for your normal use later.
   - You should see text streaming:   '<time stamp> Title, flying goat pose'
   - Let it run to confirm a text editor 'notepad' process opens with the transcribed text.   Sometimes this opens below other windows so check the taskbar for notepad processes.
   - Click in the run window 'speak_write.py - Shortcut' and press 'enter' when you're ready to close the run window
   - You will be copying from this type of 'notepad' window into your writing!

#### To make the shortcut do the following:
   - Browse to 'fwgWhisper.'
   - run `python3 setuplinux.py`
   - You will now see a new file 'speak_write' shortcut on the desktop
   - Right-click on 'speak_write' and open with an editor.  It will look something like, with your username in place of '<user>'.

```
[Desktop Entry]
Name=speak_write
Type=Application
Path=/home/<username>/
Comment=speak_write
Terminal=true
Icon=/home/<username>/.local/lib/python3.10/site-packages/pyshortcuts/icons/py.ico
Exec=/usr/bin/python3.10 /home/<user>/Documents/GitHub/fwgWhisper/speak_write.py 
```
   - Change the 'Path' line to something more useful so that it opens to where your recordings are:
```
Path=/home/<username>/Documents/GitHub/fwgWhisper
```
   - After you run this once in a location of audio files, edit 'speak_write.pref' to change the model.

```
Exec=/usr/bin/python3.10 /home/<username>/Documents/GitHub/fwgWhisper/speak_write.py small.en
``` 

[Back to Linux INSTALL](INSTALL_linux.md)

[Back to Linux](FAQ_linux.md)

[Back to top](../README.md)

