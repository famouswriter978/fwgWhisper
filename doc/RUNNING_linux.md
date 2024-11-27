# Running Linux 'whisper'
We're going to make this all run with a mouse click by creating a shortcut.

[Back to Linux INSTALL](INSTALL_linux.md)

[Back to Linux](FAQ_linux.md)

[Back to top](../README.md)

#### Before making the shortcut, try it in a shell to make sure it works.
``` commandline
cd Documents/GitHub/fwgWhisper
python3 GUI_Speak_Write.py
```
   - Ensure there are no failures in the checks.  You will know it has passed if it pops up a file selection box
   - Select one of the test files that came with 'fwgWhisper.'  The file 'FGP_160kbps_m4a.m4a' file is a good, short choice.
   - Select a model.  'tiny.en' is a good quick test.  'small.en' gives very good results for your normal use later.
   - You should see text streaming:   '<time stamp> Title, flying goat pose'
   - Let it run to confirm a text editor 'notepad' process opens with the transcribed text.   Sometimes this opens below other windows so check the taskbar for notepad processes.
   - Click in the run window 'GUI_Speak_Write.py - Shortcut' and press 'enter' when you're ready to close the run window
   - You will be copying from this type of 'notepad' window into your writing!

#### To make the shortcut do the following:
   - Browse to 'fwgWhisper.'
   - run `install.py`
   - You will now see a new files 'whisper_to_write' and 'GUI_Speak_Write' shortcut on the desktop
   - Right-click on 'GUI_Speak_Write' and open with an editor.  It will look something like, with your username in place of '<user>'.

```
[Desktop Entry]
Name=GUI_Speak_Write
Type=Application
Path=/home/<username>/
Comment=GUI_Speak_Write
Terminal=true
Icon=/home/<username>/.local/lib/python3.10/site-packages/pyshortcuts/icons/py.ico
Exec=/usr/bin/python3.10 /home/<user>/Documents/GitHub/fwgWhisper/GUI_Speak_Write.py 
```
   - Change the 'Path' line to something more useful so that it opens to where your recordings are:
```
Path=/home/<username>/Documents/GitHub/fwgWhisper
```
   - Follow instructions on screen (red text) to install for first time.
   - After you run this once in a location of audio files, edit 'GUI_Speak_Write.pref' to change the model.

```
Exec=/usr/bin/python3.10 /home/<username>/Documents/GitHub/fwgWhisper/GUI_Speak_Write.py small.en
``` 

You can ignore ALSA messages that this 'GUI_Speak_Write' throws.  It's looking for sound cards.  We're only using the microphone.

[Back to Linux INSTALL](INSTALL_linux.md)

[Back to Linux](FAQ_linux.md)

[Back to top](../README.md)

