#! /bin/sh
"exec" "`dirname $0`/venv/bin/python3" "$0" "$@"
import os
# #! /Users/daveg/Documents/GitHub/fwgWhisper/venv/bin/python3
# The #! operates for macOS only. 'Python Launcher' (Python Script Preferences) option for 'Allow override with #! in script' is checked.
#  Graphical interface to whisper:  dictate, read file, transcribe
#  Run in PyCharm
#     or
#  'python3 GUI_speak_write.py'
#
#  2023-May-04  Dave Gutz   Create
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
import sys
import tkinter.filedialog
import tkinter.messagebox
from RawRecorder import Recorder
import pyaudio
import pydub
from whisper_to_write import *
from threading import Thread
from datetime import datetime
from pvrecorder import PvRecorder
from Begini import Begini
result_ready = 0
thread_active = 0
if sys.platform == 'darwin':
    import ttwidgets as tktt
else:
    import tkinter as tk

plat = sys.platform
if plat == 'linux':
    username = os.getlogin()
    default_dr = os.path.join('/home', username, 'Recordings')
elif plat == 'darwin':
    username = os.path.expanduser('~')
    default_dr = os.path.join(username, 'Recordings')
else:
    username = os.path.expanduser('~')
    default_dr = os.path.join(username, 'Recordings')
if not os.path.exists(default_dr):
    os.makedirs(default_dr)

def_dict = {
    'Root Preferences': {
        "recordings_path": default_dr,
    },
}

# Wrap thread class so can extract resulting filename
class CustomThread(Thread):
    def __init__(self, audio_path, waiting, silent, recordings_folder, eyed):
        Thread.__init__(self)
        self.waiting = waiting
        self.silent = silent
        self.audio_path = audio_path
        self.result_path = None
        self.recordings_folder = recordings_folder
        self.id = eyed

    def run(self):
        global result_ready
        global thread_active
        thread_active += 1
        self.result_path, ready = whisper_to_write(model='', device='cpu', file_in=self.audio_path,
                                                   waiting=self.waiting, silent=self.silent,
                                                   conversation=ex_root.conversation.get())
        if self.result_path is not None and ready is True:
            result_ready += 1
            print("Results displayed automatically at 'Quit' or by pressing 'Show All'")
        thread_active -= 1
        if result_ready > 0:
            show_button.config(bg="green")
        else:
            show_button.config(bg="lightgray")


# Executive class to control the global variables
class ExRoot:
    def __init__(self, cf_=None):
        self.cf = cf_
        self.script_loc = os.path.dirname(os.path.abspath(__file__))

        config_txt = 'GUI_Speak_Write.ini'
        if sys.platform == 'linux':
            self.username = os.getlogin()
            self.config_path = os.path.join('/home', self.username, '.local', config_txt)
        elif sys.platform == 'darwin':
            self.username = os.path.expanduser('~')
            self.config_path = os.path.join(self.username, '.local', config_txt)
        else:
            self.config_path = os.path.join(os.getenv('LOCALAPPDATA'), config_txt)
        print('config file', self.config_path)

        self.root_config = None
        self.rec_folder = self.cf['Root Preferences']['recordings_path']
        self.root_config = None
        self.load_root_config(self.config_path)
        self.conversation = None

    def select_recordings_folder(self):
        print('before', self.rec_folder)
        ask_rec_folder = tk.filedialog.askdirectory(title="Select a Recordings Folder", initialdir=self.rec_folder)
        print('after askdirectory', self.rec_folder)
        if ask_rec_folder != '':
            self.rec_folder = ask_rec_folder
        os.chdir(self.rec_folder)
        print('changed working directory to', self.rec_folder)
        folder_button.config(text=self.rec_folder)
        before_folder = self.root_config['Root Preferences']['recordings_path']
        self.root_config.set('Root Preferences', 'recordings_path', self.rec_folder)
        after_folder = self.root_config['Root Preferences']['recordings_path']
        self.save_root_config(self.config_path)
        print('Changed recordings folder from\n', before_folder, '\nto\n', after_folder)

    def load_root_config(self, config_file_path):
        self.root_config = configparser.ConfigParser()
        if os.path.isfile(config_file_path):
            self.root_config.read(config_file_path)
        else:
            cfg_file = open(config_file_path, 'w')
            self.root_config.add_section('Root Preferences')
            rec_folder_path = os.path.expanduser('~') + '/Documents/Recordings'
            if not os.path.exists(rec_folder_path):
                os.makedirs(rec_folder_path)
            self.root_config.set('Root Preferences', 'recordings_path', rec_folder_path)
            self.root_config.write(cfg_file)
            cfg_file.close()
        self.rec_folder = self.root_config['Root Preferences']['recordings_path']
        print('Recordings folder is', self.rec_folder)
        return self.root_config

    def save_root_config(self, config_path_):
        if os.path.isfile(config_path_):
            cfg_file = open(config_path_, 'w')
            self.root_config.write(cfg_file)
            cfg_file.close()
            print('Saved', config_path_)
        return self.root_config


class MyRecorder:
    def __init__(self, rec_path, channels=1, rate=44100, frames_per_buffer=1024, format_out='mp3'):
        self.recorder = Recorder(channels=channels, rate=rate, frames_per_buffer=frames_per_buffer)
        self.file_path = None
        self.audio_path = None
        self.txt_path = None
        self.rec_path = rec_path
        self.running = None
        self.format_out = format_out
        self.thd_num = -1
        self.thread = []
        self.result_file = None
        self.dictate_button = None
        self.stop_button = None

    def show(self):
        global result_ready
        if thread_active > 0:
            print('wait for dictation processes to end')
        else:
            for i in range(self.thd_num+1):
                self.thread[i].join()
                if self.thread[i].result_path is not None:
                    display_result(self.thread[i].result_path, platform.system(), False, conversation=ex_root.conversation.get())
                    print('stopped thread', i, ': result in', self.thread[i].result_path)
                    result_ready -= 1  # Clear
                    self.thread[i].result_path = None  # Clear
                else:
                    print('stopped thread', i, ': result was screened')
            if result_ready > 0:
                show_button.config(bg="green")
            else:
                show_button.config(bg="lightgray")

    def start(self):
        self.file_path = os.path.join(self.rec_path, 'test.wav')
        self.txt_path = self.file_path.replace('wav', 'txt')
        if self.running is not None:
            print('already recording')
        else:
            self.running = self.recorder.open(self.file_path)
            self.running.start_recording()
            print('started recording', self.file_path)
            self.dictate_button.config(bg="lightgray")
            self.stop_button.config(bg="black")

    def stop(self):
        if self.running is not None:
            file_name = 'speak-write' + str(datetime.now()).replace(':', '-').replace('.', '-') + '.mp3'
            self.audio_path = os.path.join(self.rec_path, file_name)
            self.running.stop_recording()
            self.running.close()
            self.running = None
            self.dictate_button.config(bg="red")
            self.stop_button.config(bg="lightgray")
            print('Stopped recording; audio output in ', self.file_path)
            pydub.AudioSegment.from_wav(self.file_path).export(self.audio_path, format=self.format_out)
            try:
                os.remove(self.file_path)
                print('Converted', self.file_path, 'to', self.audio_path)
                self.thd_num += 1
                self.thread.append(CustomThread(self.audio_path, False, True, self.rec_path, self.thd_num))
                print('starting thread', self.thd_num, end='...')
                self.thread[self.thd_num].start()
            except OSError:
                print('Conversion from', self.file_path, 'to', self.audio_path, 'failed')
                pass
        else:
            print('recorder was not running')


# Global functions
def make_exit():
    show_all()
    master.destroy()


def quitting():
    if thread_active > 0:
        print('wait for conversions to end')
        msg_box = tk.messagebox.askquestion('Busy converting...', 'Whisper is busy converting a file.  Do you want to exit right away?',
                                            icon='warning')
        if msg_box == 'yes':
            make_exit()
    elif recorder.running is not None:
        print('Do you wish to stop?')
        msg_box = tk.messagebox.askquestion('Busy dictating...', 'Do you want to stop and exit right away?',
                                            icon='warning')
        if msg_box == 'yes':
            recorder.stop()
        else:
            print('Continuing to record')
    else:
        make_exit()


def select_recordings_folder():
    ex_root.select_recordings_folder()


def show_all():
    recorder.stop()
    recorder.show()


def start():
    recorder.start()


def stop():
    print('pressed stop')
    recorder.stop()


def transcribe():
    global thread_active
    if thread_active > 0:
        print('wait for dictation processes to end')
    else:
        try:
            whisper_to_write(file_in=None, waiting=False, silent=False, conversation=ex_root.conversation.get())
        except OSError:
            print('Transcription failed')
            pass


if __name__ == '__main__':
    # Configuration for entire folder selection read with filepaths
    if sys.platform != 'linux' and check_install(platform.system()) != 0:
        # Ask for input to force hold to see stderr
        print(Colors.fg.red, 'Installation problems.   See messages in window')
        tk.messagebox.showerror(message='Installation problems.   See  messages in window')
        exit(0)

    cwd_path = os.getcwd()
    cf = Begini(__file__, def_dict)
    ex_root = ExRoot(cf_=cf)
    recorder = MyRecorder(ex_root.rec_folder)

    # Get/check microphone
    mic_avail = True
    try:
        # audio_devices = PvRecorder.get_audio_devices() dag 10/29
        audio_devices = PvRecorder.get_available_devices()
        for index, device in enumerate(audio_devices):
            print(f"[{index}] {device}")
        pa = pyaudio.PyAudio()
        default = pa.get_default_input_device_info()  # raises IOError
        print('using', default['name'])
    except IOError:
        print(Colors.fg.red, 'Default microphone not found.  Capability limited', Colors.reset)
        mic_avail = False

    # Define frames
    master = tk.Tk()
    master.maxsize(380, 800)
    master.title('openAI whisper')
    icon_path = os.path.join(ex_root.script_loc, 'fwg.png')
    master.iconphoto(False, tk.PhotoImage(file=icon_path))

    # Checks
    bg_color = "lightgray"
    box_color = "lightgray"
    relief = tk.FLAT

    outer_frame = tk.Frame(master, bd=5, bg=bg_color)
    outer_frame.pack(fill='x')

    pic_frame = tk.Frame(master, bd=5, bg=bg_color)
    pic_frame.pack(fill='x')

    pad_x_frames = 1
    pad_y_frames = 2

    recordings_frame = tk.Frame(outer_frame, width=250, height=200, bg=box_color, bd=4)
    recordings_frame.pack(side=tk.TOP)

    dictation_frame = tk.Frame(outer_frame, width=250, height=100, bg=box_color, bd=4, relief=relief)
    dictation_frame.pack(side=tk.TOP)

    transcription_frame = tk.Frame(outer_frame, width=250, height=100, bg=box_color, bd=4, relief=relief)
    transcription_frame.pack(side=tk.TOP)

    conversation_frame = tk.Frame(outer_frame, width=250, height=100, bg=box_color, bd=4, relief=relief)
    conversation_frame.pack(side=tk.TOP)

    quit_frame = tk.Frame(outer_frame, width=250, height=100, bg=box_color, bd=4, relief=relief)
    quit_frame.pack(side=tk.TOP)

    folder_label = tk.Label(recordings_frame, text='Recordings path', bg=box_color, fg="blue")
    folder_label.pack()
    if platform.system() == 'Darwin':
        folder_button = tktt.TTButton(recordings_frame, text=ex_root.rec_folder, command=select_recordings_folder,
                                      fg="blue", bg=bg_color)
    else:
        folder_button = tk.Button(recordings_frame, text=ex_root.rec_folder, command=select_recordings_folder,
                                  fg="blue", bg=bg_color)
    folder_button.pack(ipadx=5, pady=5)

    if mic_avail:
        button_spacer = tk.Label(dictation_frame, text=' ', bg=bg_color)
        button_spacer.pack(side="left", fill='x', expand=True)

        if platform.system() == 'Darwin':
            recorder.dictate_button = tktt.TTButton(dictation_frame, text='Dictate', command=start, bg="red", fg="white")
        else:
            recorder.dictate_button = tk.Button(dictation_frame, text='Dictate', command=start, bg="red", fg="white")
        recorder.dictate_button.pack(side="left", fill='x', expand=True)

        button_spacer = tk.Label(dictation_frame, text='          ', bg=bg_color)
        button_spacer.pack(side="left", fill='x', expand=True)

        if platform.system() == 'Darwin':
            recorder.stop_button = tktt.TTButton(dictation_frame, text='Stop', command=stop, bg="lightgray", fg="white")
        else:
            recorder.stop_button = tk.Button(dictation_frame, text='Stop', command=stop, bg="lightgray", fg="white")
        recorder.stop_button.pack(side="left", fill='x', expand=True)
    else:
        if platform.system() == 'Darwin':
            button_recorder = tktt.Button(dictation_frame, text='NO MIC')
        else:
            button_recorder = tk.Button(dictation_frame, text='NO MIC')
        button_recorder.pack(side="left", fill='x', expand=True)

    button_spacer = tk.Label(transcription_frame, text='  ', bg=bg_color)
    button_spacer.pack(side="left", fill='x', expand=True)
    if platform.system() == 'Darwin':
        trans_recorder = tktt.TTButton(transcription_frame, text='Transcribe File(s)', command=transcribe, fg="green",
                                       bg=bg_color)
    else:
        trans_recorder = tk.Button(transcription_frame, text='Transcribe File(s)', command=transcribe, fg="green",
                                   bg=bg_color)
    trans_recorder.pack(side="left", fill='x', expand=True)

    ex_root.conversation = tk.BooleanVar()
    converse_button = tk.Checkbutton(conversation_frame, text='Conversation', bg=bg_color, variable=ex_root.conversation,
                                     onvalue=True, offvalue=False)
    converse_button.pack(fill='x', expand=True)

    button_spacer = tk.Label(quit_frame, text=' ', bg=bg_color)
    button_spacer.pack(side="left", fill='x', expand=True)
    if platform.system() == 'Darwin':
        show_button = tktt.TTButton(quit_frame, text='Show All', command=show_all, fg="white", bg="lightgray")
    else:
        show_button = tk.Button(quit_frame, text='Show All', command=show_all, fg="white", bg="lightgray")
    show_button.pack(side="left", fill='x', expand=True)

    button_spacer = tk.Label(quit_frame, text='          ', bg=bg_color)
    button_spacer.pack(side="left", fill='x', expand=True)
    quit_button = tk.Button(quit_frame, text='Quit', command=quitting, bg=bg_color)
    quit_button.pack(side="left", fill='x', expand=True)

    pic_path = os.path.join(ex_root.script_loc, 'speak_write.png')
    image = tk.Frame(pic_frame, borderwidth=2, bg=box_color)
    image.pack(side=tk.TOP, fill="x")
    image.picture = tk.PhotoImage(file=pic_path)
    image.label = tk.Label(image, image=image.picture)
    image.label.pack()

    # Begin
    master.mainloop()
