# Special Developer Instructions
[Back to top](../README.md)

A very convenient way to debug the 'whisper-to-write' program that the user normally runs with 'python3.10 whisper-to-write.py' is to use PyCharm.  This is an IDE that can run either in isolated Python mode or call upon the System Python.  Very handy.   Using the System Interpreter means that you don't have to install another huge python program.   But a 'Virtual Environment' - 'venv' is often needed to debug nasty problems related to the Python installation.

  - Download [pycharm-community](https://www.jetbrains.com/pycharm/download/#section=windows) selecting the 'Community' free edition on the 'Download' button.
  - Install it and 'Open project' at the 'fwgWhisper' folder.
  - Select Interpreter - System.  It should automatically pick up the dependencies running after installation the dependencies above.   If not, you have a new clue!
  - Wait for all the 'skeleton' and 'indexing' functions to end before running the first time
  - Doubleclick on 'whisper-to-write.py.'  Right-click in 'whisper-to-write.py' and pick 'Run whisper-to-write'
  - After the first run you can just use the arrows in the toolbar at top
  - Add print statements, use the debugging features, whatever....

#### Virtual environment
  - To install a 'venv' open the settings, select 'local interpreter' and 'venv'.   Add dependencies using the '+' operator:  'configparser' and 'openai-whisper'


#### GitHub desktop
It is also useful to work with actual source using GitHub.  You can find the installation stuff [here.](https://docs.github.com/en/desktop/installing-and-configuring-github-desktop/installing-and-authenticating-to-github-desktop/installing-github-desktop
)

[Back to top](../README.md)
