# FAQ for windows whisper
[Back to fwgWhisper](../README.md)

## How do I install?
Synopsis:  Download the repository from the [top level](../README.md).   Put it in Documents/GitHub folder.
Download and install ffmpeg.   Download and install python3.10.10.  Use 'pip' and 'pip3' from
'python3.10' to install dependencies 'configparser' and 'openai-whisper' respectively.  
Start Google Drive if installed.  Then run 'whisper-to-write.py' using 'python3.10.'

[Details](INSTALL_windows.md)


## Running it:  how?
You can run it two ways from easiest to hardest:
1. Shortcut that points to `python whisper-to-write.py`.  Runs multiple files - only mouse clicks, truly.
2. From a terminal as `python whisper-to-write.py`.   Of course, you'll have to type the full path or start from the folder by 'cd' first.  Runs multiple files

The first run creates a preferences file 'whisper-to-write.pref' in the folder where the audio files are.   You may edit this to change the AI model.   There is a balance between accuracy and speed.

The first run with a new model also loads the model into your '$HOME/.cache' folder.


## Error message - 'Opening registry... \DriveFS\Share failed with 0x2'
This happens when Google Drive is installed but not running when the fileopenbox of whisper-to-write.py is executed.
The solution is to start Drive e.g. Start or Search - Drive - Google Drive App


## Shortcut:  how do I make one?
Browse to the folder with whisper-to-write.py in it.  right-click on whisper-to-write.py, select Other, click Create Shortcut.   Move the
resulting file to your desktop or wherever you want it.


## My python installation is not found
If `python3` and `python` do not work from the command line, you need to add the PATH parameter manually:
   - Open 'Edit environment variables for your account' in start menu
   - Select 'Environment variables' then 'Path' - 'Edit' in the top user area. 
   - Add two lines and 'move up' so they're the first two entries.  Select 'OK' and 'OK'
```
        %USERPROFILE%\AppData\Local\Programs\Python\Python310\
        %USERPROFILE%\AppData\Local\Programs\Python\Python310\Scripts\
```
   - Try again

[Back to top](../README.md)
