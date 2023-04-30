# FAQ for macOS whisper
[Back to fwgWhisper](../README.md)

## How do I install?
Synopsis:  Download this repository.   Put it in Documents/GitHub folder.
Download and install ffmpeg.   Download and install python3.10.10.  Use 'pip' and 'pip3' from
'python3.10' to install dependencies 'configparser' and 'openai-whisper' respectively.  
Start Google Drive if installed.  Then run 'whisper-to-write.py' using 'python3.10.'

Details:  [INSTALL macOS](INSTALL_macos.md).


## Running it:  how?
You can run it two ways from easiest to hardest:
1. Shortcut that points to `python3 whisper-to-write.py`.  Runs multiple files - only mouse clicks, truly.
2. From a terminal as `python3 whisper-to-write.py`.   Of course, you'll have to type the full path or start from the folder by 'cd' first.  Runs multiple files

The first run creates a preferences file 'whisper-to-write.pref' in the folder where the audio files are.   You may edit this to change the AI model.   There is a balance between accuracy and speed.

The first run with a new model also loads the model into your '$HOME/.cache' folder.


## Shortcut:  how do I make one?
Browse to the folder with whisper-to-write.py in it.  right-click on whisper-to-write.py, select Other, click Create Shortcut.   Move the
resulting file to your desktop or wherever you want it.

## ffmpeg not found
Installation of ffmpeg is difficult, for some reason.   There is path mangling and some code calls the executable and other calls native python.   The following usually resets everything and fixes it.
```commandline
python3 -m pip uninstall ffmpeg
python3 -m pip uninstall ffmpeg-python
pip uninstall ffmpeg-python
pip uninstall ffmpeg
brew uninstall ffmpeg
python3 -m pip install ffmpeg-python
brew install ffmpeg
```


## How do I improve the accuracy?
Browse to the folder with your audio files in it.   Open the file 'whisper-to-write.prefs' and change 'model' as instructed by the 'model remark' line above it.  The choices are ordered from the lowest resolution to highest, also the lowest size to highest and the fastest to slowest.

Here's a sample [whisper-to-write.pref file](../samples_good/whisper-to-write.pref)

[Back to top](../README.md)

