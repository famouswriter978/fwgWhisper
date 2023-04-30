# INSTALL for Windows 'whisper'
[Back to Windows](FAQ_windows.md)

[Back to top](../README.md)

Synopsis:  Download this repository.   Put it in Documents/GitHub folder.
Download and install ffmpeg.   Download and install python3.10.10.  Use 'pip' and 'pip3' from
'python3.10' to install dependencies 'configparser' and 'openai-whisper' respectively.  The paths will get set automatically to point 'python' at 'python3.10'.
Start Google Drive if installed.  Then run 'whisper-to-write.py' using 'python'

Be sure that your user account name has no spaces before starting this.   If it does, change it now.   Go to 'Control Panel - User Accounts - Change the account name'

## Download the repository [fwgWhisper](http://www.github.com/davegutz/fwgWhisper)
For most people it's easiest to click on the green '<> Code' box and download the '.zip' file.  Extract to Documents/GitHub.  Make that folder if you need to.  When done, there will be a folder similar to 'fwgWhisper-main' where 'main' refers to the Current Branch in GitHub.  Install and use [NanaZip](https://apps.microsoft.com/store/detail/nanazip/9N8G7TSCL18R?hl=en-us&gl=us&rtc=1)

If you're so inclined, use the GitHub desktop app to perform this download.  If you don't know what I'm talking about, use the method above.


### Install python3
'python3.10.10' is what I used to develop these instructions.

1. See what you have:  Open a PowerShell or CMD shell.   Type  `python3` then if that is blank try `python`.   It will say which version in the first line.  You need 3.10 or greater.  Type `ctrl-z` and possibly `ENTER` to exit the python shell.
2. Go to the [python website](https://www.python.org/downloads/) and get 3.10.10.
3. Double-click on the python<>.exe file in Downloads
4. Check 'Add python.exe to PATH' option.   If this is the first install of a python3 it will exist as 'python3' otherwise as 'python3.10'
5. When done try `python3` then if that is blank try `python`.  You may need to restart the shell window.  Type `ctrl-z` and possibly `ENTER` to exit the python shell.

If `python3` and `python` do not work from the command line, you need to add the PATH parameter manually:
   - Open 'Edit environment variables for your account' in start menu
   - Select 'Environment variables' then 'Path' - 'Edit' in the top user area. 
   - Add two lines and 'move up' so they're the first two entries.  Select 'OK' and 'OK'
```
        %USERPROFILE%\AppData\Local\Programs\Python\Python310\
        %USERPROFILE%\AppData\Local\Programs\Python\Python310\Scripts\
```
   - Open a NEW PowerShell window and try the previous `python3` or `python` steps again.


## Install the dependencies using 'pip'
Open a non-administrative Power Shell, Terminal (Win 11), or Cmd and run the following anywhere (use 'python3' if needed from previous step).

```commandline
python -m pip install --upgrade pip
python -m pip install configparser
python -m pip install openai-whisper --default-timeout=1000
```

### Running:  [here](RUNNING_windows.md)

### Special Developer Instructions:  [here](DEVELOPER.md)

[Back to Windows](FAQ_windows.md)

[Back to top](../README.md)

