# INSTALL and run for macOS 'whisper'
[Back to macOS](FAQ_macos.md)

[Back to top](../README.md)

Synopsis:  Download this repository.   Put it in Documents/GitHub folder.
Download and install ffmpeg-python (or ffmpeg...TBD).   Download and install python3.10.10.  Use 'pip' and 'pip3' from
'python3.10' to install dependencies 'configparser' and 'openai-whisper' respectively.

Then run 'whisper-to-write.py' using 'python3.10.'

# INSTALL

### Download the repository [fwgWhisper](http://www.github.com/davegutz/fwgWhisper)
For most people it's easiest to click on the green '<> Code' box and download the '.zip' file.  Extract to Documents/GitHub.  Make that folder if you need to.  When done, there will be a folder similar to 'fwgWhisper-main' where 'main' refers to the Current Branch in GitHub.  Install and use [NanaZip](https://apps.microsoft.com/store/detail/nanazip/9N8G7TSCL18R?hl=en-us&gl=us&rtc=1), I recommend, if you need such a tool to unpack fwgWhisper.

If you're so inclined, use the GitHub desktop app to perform this download.  If you don't know what I'm talking about, use the method above.


### Install python3
'python3.10.10' is what I used to develop these instructions.  Later releases should work.

1. See what you have:  `python3`   It will say which version in the first line.  You need 3.10 or greater to run the tools provided herein.  Type `ctrl-z` and possibly `ENTER` to exit the python shell.
2. Go to the [python website](https://www.python.org/downloads/) and get what you need.  Install as instructed.


### Install 'brew'
Go [here.](https://brew.sh/)
This was the command at the time of this writing:

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`


### Install the python dependencies using 'python pip' and 'brew'
Open a terminal (Launchpad - terminal) and run the following as yourself no matter where it opens to

```
python3 -m pip install --upgrade pip
python3 -m pip install configparser
python3 -m pip install openai-whisper --default-timeout=1000  # Install 'whisper' and 'ffmpeg'
python3 -m pip install ffmpeg-python
python3 certifi_glob.py  # Install certificates
brew install ffmpeg
```

### Running:  [here](RUNNING_macos.md)

### Special Developer Instructions:  [here](DEVELOPER.md)

[Back to macOS](FAQ_macos.md)

[Back to top](../README.md)
