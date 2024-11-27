# INSTALL and run for Linux 'whisper'
[Back to Linux](FAQ_linux.md)

[Back to top](../README.md)

## INSTALL
Synopsis:  Download this repository.   Put it in Documents/GitHub folder.
Download and install ffmpeg.   Download and install python3.10.10 if at least 3.10.6 is not installed.  Use 'pip' and 'pip3' from
'python3.10' to install dependencies 'configparser', 'opengui', and 'openai-whisper' respectively.

Then run 'whisper_to_write.py' using 'python3.10.'


### Download the repository [fwgWhisper](http://www.github.com/famouswriter978/fwgwhisper)
For most people it's easiest to click on the green '<> Code' box and download the '.zip' file.  Extract to Documents/GitHub.  Make that folder if you need to.  When done, there will be a folder similar to 'fwgWhisper' where 'main' refers to the Current Branch in GitHub.

If you're so inclined, use the GitHub desktop app to perform this download.  If you don't know what I'm talking about, use the method above.


### Perform a standard update to ensure dependencies are the latest
`sudo apt update && sudo apt upgrade`


### Add .local/bin to paths
Edit '.bashrc' and put the following at the bottom:

```
# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi
```
Close and reopen any terminal windows to incorporate the new PATH.   Alternatively you could run in any open terminal:
`. ~/.bashrc`


### Install python3
'python3.10.6' is what I used to develop these instructions.  I tried to use venv in PyCharm but the pyCharm manager would not install 'openai-whisper'.

1. See what you have:  `python3`   It will say which version in the first line.  You need 3.10 or greater.  Known to work with 3.10.6 and 3.10.10.  Type `ctrl-z` and possibly `ENTER` to exit the python shell.
2. Go to the [python website](https://www.python.org/downloads/) and get what you need.  Install as instructed.


### Install the dependencies using 'pip'
Open a terminal (Launchpad - terminal) and run the following as yourself no matter where it opens to

```
# open pyCharm.
   - Setup local interpreter pointing to a python >=3.8 and <3.12.
   - You can find instructions for installing a new interpreter here:
   https://drive.google.com/open?id=1-ANANsynB4KywgxAkJ2sMGLSDicpdLdo&usp=drive_fs
   - Pop!_OS is slightly different as covered here:
        https://drive.google.com/open?id=1Nu-Jjj5KC27_ov1M4e8BTsm9PFwOTfmk&usp=drive_fs
   - Summary of pyCharm setup
        sudo apt install python3-dev, portaudio19-dev, ffmpeg, libssl-dev, libsound-dev, python3-tk
        # start pycharm-community using command line
        # set Help - Change Memory Settings - 4096 (for openai-whisper install)
        # point at python interpreter, load packages:  ffmpeg-python, openai-whisper, pvrecorder, pvdub, pvaudio
	    # Run 'speak_write.py'.  When it works, run 'install.py'.
   - For any linux operating system let pyCharm find the missing dependencies
```

### Running:  [here](RUNNING_linux.md)

# Running
We're going to make this all run with a mouse click by creating a shortcut.

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
   - Click in the run window 'whisper_to_write.py - Shortcut' and press 'enter' when you're ready to close the run window
   - You will be copying from this type of 'notepad' window into your writing!

#### To make the shortcut do the following:
   - Browse to 'fwgWhisper.'
   - run `python3 install.py` (or in pyCharm)
   - follow instructions in output

   - If you want, make life easier by adding 'small.en' after the 'Target:' data to force it to always run the excellent small model without having to select it everytime the program runs

   - 'Exec=/usr/bin/python3.10 /home/<username>/Documents/GitHub/fwgWhisper/whisper_to_write.py small.en

### Special Developer Instructions:  [here](DEVELOPER.md)

[Back to Linux](FAQ_linux.md)

[Back to top](../README.md)
