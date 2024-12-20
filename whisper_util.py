#  Utilities for myWhisper
#  2023-Apr-13  Dave Gutz   Create
# Copyright (C) 2023 Dave Gutz and Sarah E. Gutz
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# See http://www.fsf.org/licensing/licenses/lgpl.txt for full license text.
import os
import sys
import json
import inspect
import subprocess
import configparser
import importlib.metadata
from Colors import Colors
from mbox import MessageBox
from typing import Callable, TextIO

# Filetype definitions
supported = ['.mp3', '.m4a', '.mp4', '.mpeg', '.mpga', '.opus', '.ts', '.voc', '.w64', '.wav',
             '.webm', '.wma', '.wv']
unsupported = ['.ac3', '.aac', '.aiff', '.au', '.caf', '.flac', '.mp2', '.oga', '.ogg', '.sln']
unsupported_no_msg = ['.txt', '.pdf', '.py', '.md']


def str2bool(string):
    str2val = {"True": True, "False": False}
    if string in str2val:
        return str2val[string]
    else:
        raise ValueError(f"Expected one of {set(str2val.keys())}, got {string}")


def optional_int(string):
    return None if string == "None" else int(string)


def optional_float(string):
    return None if string == "None" else float(string)


system_encoding = sys.getdefaultencoding()
if system_encoding != "utf-8":
    def make_safe(string):
        # replaces any character not representable using the system default encoding with an '?',
        # avoiding UnicodeEncodeError (https://github.com/openai/whisper/discussions/729).
        return string.encode(system_encoding, errors="replace").decode(system_encoding)
else:
    def make_safe(string):
        # utf-8 can encode any Unicode code point, so no need to do the round-trip encoding
        return string


# Make the installation as easy as possible
# Assume that we're either starting with a good python installation
#   or
# a working PyCharm installation
def check_install(platform, pure_python=True):
    print("checking for dependencies...", end='')

    # Check status
    if platform == 'Darwin' or platform == 'Windows' or platform == 'Linux':
        have_python = check_install_python(platform)
        print(f"{have_python=}")
        have_whisper = check_install_whisper(pure_python)
        have_ffmpeg = check_install_ffmpeg(pure_python)
        print(f"{have_whisper=}\n{have_ffmpeg=}")
        have_ffmpeg_windows = False
        if platform == 'Windows':
            have_ffmpeg_windows = check_install_ffmpeg(pure_python=False)
            if have_ffmpeg_windows == -1:
                have_ffmpeg_windows = False
            else:
                have_ffmpeg_windows = True
                print('have ffmpeg')
        print('')

        # python help
        if not have_python:
            python_help(platform)

        # whisper / ffmpeg help:   openai-whisper installs them
        if not have_whisper or not have_ffmpeg or\
                (platform == 'Windows' and not have_ffmpeg_windows):
            whisper_help(platform, have_whisper, have_ffmpeg, have_ffmpeg_windows)

        # All good
        # #########Interim don't worry about macOS
        # If we have_python and have_whisper and have_ffmpeg:
        if have_python and have_whisper and have_ffmpeg and \
                (platform != 'Windows' or have_ffmpeg_windows):
            return 0
        else:
            return -1
    else:
        print(Colors.fg.red, "platform '", platform, "' unknown.   Contact your administrator", Colors.reset)
        return -1


# Check installation status of ffmpeg
def check_install_ffmpeg(pure_python=True, verbose=False):
    if pure_python:
        have = check_install_pkg('ffmpeg')
    else:
        test_cmd = 'ffmpeg -version'
        if verbose:
            print('')
            print("checking for {:s}...".format(test_cmd), end='')
        have = run_shell_cmd(test_cmd, silent=True)
    if have is False:
        print(Colors.fg.red, 'failed')
        print(Colors.fg.green, 'Install ffmpeg', Colors.reset)
    else:
        if verbose:
            print('success')
    return have


def check_install_pkg(pkg, verbose=False):
    if verbose:
        print("checking for {:s}...".format(pkg), end='')
    installed_packages = importlib.metadata.packages_distributions()
    return installed_packages.__contains__(pkg)


# Check installation status of python
def check_install_python(platform, verbose=False):
    have_python = False
    if platform == 'Darwin':
        test_cmd_python = 'python3 --version'
    elif platform == 'Windows':
        test_cmd_python = 'python --version'
    elif platform == 'Linux':
        test_cmd_python = 'python3 --version'
    else:
        raise Exception('platform unknown.   Contact your administrator')
    if verbose:
        print('')
        print("checking for {:s}...".format(test_cmd_python), end='')
    result = run_shell_cmd(test_cmd_python, silent=True, save_stdout=True)
    if result == -1:
        print('failed')
    else:
        ver = result[0].split('\n')[0].split(' ')[1]
        ver_no = int(ver.split('.')[0])
        rel_no = int(ver.split('.')[1])
        if result == -1 or ver_no < 3 or rel_no < 6:
            print(Colors.fg.red, 'failed')
            if ver_no < 3:
                print("System '", test_cmd_python, "' command points to version<3.  whisper needs 3", Colors.reset)
            if rel_no < 6 or rel_no > 11:
                print("System '", test_cmd_python, "' command points to release<6.  whisper needs >=6 and <=11", Colors.reset)
        else:
            have_python = True
            print('success')
    return have_python


# Check installation status of whisper
def check_install_whisper(pure_python=True, verbose=False):
    if pure_python:
        have = check_install_pkg('whisper')
    else:
        test_cmd = 'whisper --fp16 False -h'
        if verbose:
            print('')
            print("checking for {:s}...".format(test_cmd), end='')
        have = run_shell_cmd(test_cmd, silent=True, save_stdout=True)
    if have is False:
        print(Colors.fg.red, 'failed', Colors.reset)
    else:
        if verbose:
            print('success')
    return have


# Config helper function
def config_section_map(config, section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except AttributeError:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


# Work out all the paths
def configurator(filepath):
    (config_path, config_basename) = os.path.split(filepath)
    config_file_path = os.path.join(config_path, 'whisper_to_write.pref')
    config = load_config(config_file_path)
    return config_path, config_basename, config_file_path, config


# Open text file in editor
def display_result(txt_path, platform, silent, conversation=False):
    paragraph(txt_path, conversation)

    if silent is False:
        if platform == 'Darwin':
            subprocess.Popen(['open', '-a', 'TextEdit', txt_path])
        if platform == 'Linux':
            subprocess.Popen(['gedit', txt_path])
        elif platform == 'Windows':
            subprocess.Popen(['notepad', txt_path])
    else:
        print('Results in', txt_path)


# Define output write, e.g. 'file.txt'
def get_writer(
    output_format: str, output_dir: str
) -> Callable[[dict, TextIO, dict], None]:
    writers = {
        "txt": WriteTXT,
        "json": WriteJSON,
    }

    if output_format == "all":
        all_writers = [writer(output_dir) for writer in writers.values()]

        def write_all(result: dict, file: TextIO, options: dict):
            for writer in all_writers:
                writer(result, file, options)

        return write_all

    return writers[output_format](output_dir)


# Config file
def load_config(path):
    config = configparser.ConfigParser()
    if os.path.isfile(path):
        config.read(path)
    else:
        cfg_file = open(path, 'w')
        config.add_section('Whisper Preferences')
        config.set('Whisper Preferences', 'model remark',
                   'Possible values: tiny.en, base.en, small.en, medium.en, large')
        config.set('Whisper Preferences', 'model', 'small.en')
        config.write(cfg_file)
        cfg_file.close()
    return config


# Make paragraph out of jumbled file
def paragraph(txt_path, conversation=False):
    with open(txt_path, 'r') as file:
        lines = [line.rstrip() for line in file]
    file.close()
    with open(txt_path, 'w') as file:
        for line in lines:
            file.write(line)
            # APA Guidelines are for one space between sentences
            if line:
                l_ch = line[-1]
                if conversation and (l_ch == '.' or l_ch == '?' or l_ch == '!'):
                    file.write('\n')
                else:
                    file.write(' ')
    file.close()


# Help for pip install
def pip_help(platform):
    # windows
    if platform == 'Windows':
        print(inspect.cleandoc("""
            #############  Once python installed:
            python -m pip install --upgrade pip
            pip install configparser
            """), Colors.reset, sep=os.linesep)
    elif platform == 'Linux':
        python_help(platform)


# Help for python install
def python_help(platform):
    # Windows
    if platform == 'Windows':
        print(Colors.fg.green, inspect.cleandoc("""
            #############  Install python3.6+ and check path 'python --version' points to it")
            # go to:  python.org/download"
            python -m pip install --upgrade pip
            python -m pip install configparser
            python -m pip install openai-whisper --default-timeout=1000 
              or + openai-whisper
            python -m pip install ffmpeg-python
              or + ffmpeg-python
            python whisper_to_write.py
            """), Colors.reset, sep=os.linesep)
    # macOS
    if platform == 'Darwin':
        print(Colors.fg.green, inspect.cleandoc("""
            #############  Install python3.10.10 and check path 'python3 --version' points to it")
            # go to:  python.org/download"
            python3 -m pip install --upgrade pip
            python3 -m pip install configparser
            python3 -m pip install openai-whisper --default-timeout=1000 
            python3 -m pip install ffmpeg-python
            python3 certifi_glob.py
            python3 whisper_to_write.py
            """), Colors.reset, sep=os.linesep)
    # Linux
    elif platform == 'Linux':
        print(Colors.fg.green, inspect.cleandoc("""
            #############  Install python3.6+ and 3.12- check path 'python --version' points to it")
            sudo apt update && sudo apt upgrade
            sudo apt install python3.11.9
            sudo python3.10 -m pip install upgrade
            sudo pip3 install openai-whisper --default-timeout=1000
              or + openai-whisper
                + ffmpeg-python
            pip3 install configparser
            pip3 install shortcuts
            python3 whisper_to_write.py
            """), Colors.reset, sep=os.linesep)


# Structure for result writing
class ResultWriter:
    extension: str

    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def __call__(self, result: dict, audio_path: str, options: dict):
        audio_basename = os.path.basename(audio_path)
        audio_basename = os.path.splitext(audio_basename)[0]
        output_path = os.path.join(self.output_dir, audio_basename + "." + self.extension)

        with open(output_path, "w", encoding="utf-8") as f:
            self.write_result(result, file=f, options=options)

    def write_result(self, result: dict, file: TextIO, options: dict):
        raise NotImplementedError


# Run shell command showing stdout progress (special logic for Windows)
# Hope it works on Mac and Linux
def run_shell_cmd(cmd, silent=False, save_stdout=False, colorize=False):
    stdout_line = None
    if save_stdout:
        stdout_line = []
    if colorize:
        print(Colors.bg.brightblack, Colors.fg.wheat)
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            bufsize=1, universal_newlines=True)
    # Poll process for new output until finished
    while True:
        try:
            nextline = proc.stdout.readline()
        except AttributeError:
            nextline = ''
        if nextline == '' and proc.poll() is not None:
            break
        if save_stdout:
            stdout_line.append(nextline)
        if not silent:
            sys.stdout.write(nextline)
            sys.stdout.flush()
    if colorize:
        print(Colors.reset)
    if save_stdout and not silent:
        print('stdout', stdout_line)
    output = proc.communicate()[0]
    exit_code = proc.returncode
    if exit_code == 0:
        if save_stdout:
            return stdout_line
        else:
            return exit_code
    else:
        return -1


def overwrite_query(msg, b1=('yes', 'yes'), b2=('no', 'no'), b3=('all', 'all'), b4=('none', 'none'),
                    b5=('exit', 'exit'), frame_=True, t=False, entry=False):
    """Create an instance of MessageBox, and get data back from the user.
    msg = string to be displayed
    b1 = text for left button, or a tuple (<text for button>, <to return on press>)
    b2 = text for right button, or a tuple (<text for button>, <to return on press>)
    frame = include a standard outerframe: True or False
    t = time in seconds (int or float) until the msgbox automatically closes
    entry = include an entry widget that will have its contents returned: True or False
    """
    msgbox = MessageBox(msg, b1, b2, b3, b4, b5, frame_, t, entry)
    msgbox.root.mainloop()
    # the function pauses here until the mainloop is quit
    msgbox.root.withdraw()
    msgbox.root.destroy()
    return msgbox.returning


# Screen out unwanted files.   Keep track with static/global 'choice'
_choice = 'yes'


def screened(extension, source, result, basename):
    global _choice
    screen = False
    result_stat = None
    if extension in unsupported_no_msg:
        screen = True
    elif extension in unsupported:
        print(source, 'file type', extension, 'not supported.')
        print('Supported file types=', supported)
        print('Continuing...')
        screen = True
    elif extension not in supported:
        print(Colors.fg.red, extension, '?', Colors.reset)
        screen = True

    # Check if source has updated since result
    source_stat_st_mtime = os.stat(source).st_mtime
    try:
        result_stat_st_mtime = os.stat(result).st_mtime
    except OSError:
        result_stat_st_mtime = 0.0

    # Process user preference
    if _choice == 'all' or result_stat == 0.0:
        screen = False
    elif _choice == 'none':
        screen = True
    elif source_stat_st_mtime < result_stat_st_mtime:
        _choice = overwrite_query('Overwrite result file ' + basename + '?' + '\n' +
                                  "'yes' and 'no' refer to this file.  Your audio is always preserved." + '\n' +
                                  "'all' and 'none' refer to remaining result files as well. 'exit' is to quit" + '\n' +
                                  "If this file result does not exist it will be generated now unless you 'exit'.")
        if _choice == 'exit':
            print('Quitting...')
            input('\nEnter anything to close window')
            exit(0)
        elif _choice == 'yes' or _choice == 'all':
            screen = False
        elif _choice == 'no' or _choice == 'none':
            screen = True
    else:
        screen = False

    if screen:
        print('screened:  skipping', source)

    return screen


# whisper help
def whisper_help(platform, have_whisper, have_ffmpeg, have_ffmpeg_windows):

    # windows
    if platform == 'Windows':
        # windows whisper
        if not have_whisper:
            print(Colors.fg.green, inspect.cleandoc("""
                ############# Once python and pip installed, install whisper and ffmpeg by:
                pip3 install openai-whisper 
                """), Colors.reset, sep=os.linesep)

        # windows ffmpeg
        if not have_ffmpeg:
            print(Colors.fg.green, inspect.cleandoc("""
                #############  Once python and pip installed, install ffmpeg by:
                python -m pip install ffmpeg-python
                """), Colors.reset, sep=os.linesep)

        # windows ffmpeg_windows
        if not have_ffmpeg_windows:
            print(Colors.fg.green, inspect.cleandoc("""
                #############  Once python and pip installed, install ffmpeg cli by:
                see README, install ffmpeg section of Windows install
                """), Colors.reset, sep=os.linesep)

    # mac os
    if platform == 'Darwin':
        # mac os whisper
        if not have_whisper:
            print(Colors.fg.green, inspect.cleandoc("""
                #############  on MacOS using pip installed with python
                python3 -m pip install --upgrade pip
                python3 -m pip install openai-whisper --default-timeout=1000
                """), Colors.reset, sep=os.linesep)

        # mac os ffmpeg
        if not have_ffmpeg:
            print(Colors.fg.green, inspect.cleandoc("""
                #############  on MacOS using using pip installed with python
                python3 -m pip install ffmpeg-python
                """), Colors.reset, sep=os.linesep)

    # Linux
    if platform == 'Linux':
        if not have_ffmpeg or not have_whisper:
            python_help(platform)


# Write classes
class WriteJSON(ResultWriter):
    extension: str = "json"

    def write_result(self, result: dict, file: TextIO, options: dict):
        json.dump(result, file)


class WriteTXT(ResultWriter):
    extension: str = "txt"

    def write_result(self, result: dict, file: TextIO, options: dict):
        for segment in result["segments"]:
            print(segment["text"].strip(), file=file, flush=True)
