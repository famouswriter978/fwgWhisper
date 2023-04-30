# FAQ for linux whisper
[Back to fwgWhisper](../README.md)

## How do I install?
Synopsis:  Download this repository.   Put it in Documents/GitHub folder.
Download and install ffmpeg.   Download and install python3.10.10.  Use 'pip' and 'pip3' from
'python3.10' to install dependencies 'configparser' and 'openai-whisper' respectively.  
Start Google Drive if installed.  Then run 'whisper-to-write.py' using 'python3.10.'

Details:  [INSTALL_linux.md](INSTALL_linux.md).


## Running it:  how?
You can run it two ways from easiest to hardest:
1. Shortcut that points to `python3.10 whisper-to-write.py`.  Runs multiple files - only mouse clicks, truly.
2. From a terminal as `python3.10 whisper-to-write.py`.   Of course, you'll have to type the full path or start from the folder by 'cd' first.  Runs multiple files

The first run creates a preferences file 'whisper-to-write.pref' in the folder where the audio files are.   You may edit this to change the AI model.   There is a balance between accuracy and speed.

The first run with a new model also loads the model into your '$HOME/.cache' folder.

## Shortcut:  how do I make one?
Open pycharm-community.   Use System interpreter.   Run setuplinux.py.  Edit the .desktop file top
point to the audio files folder you are using.   It initializes to home.

[Back to top](../README.md)
