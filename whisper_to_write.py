#  Prototype cli interface that feeds .wav file to whisper and transcribes it to .pdf
#  Run in PyCharm
#     or
#  'python3 whisper_to_write.py'
#
#  2023-Apr-29  Dave Gutz   Create
# Copyright (C) 2023 Dave Gutz
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
# See http://www.fsf.org/licensing/licenses/lgpl.txt for full license text
import time
import timeit
import whisper
import platform
import tkinter as tk
from whisper_util import *
from tkinter import filedialog
os.environ['PYTHONIOENCODING'] = 'utf - 8'  # prevents UnicodeEncodeError: 'charmap' codec can't encode character


# Wrap the openai Whisper program to make it useful and more portable
def whisper_to_write(model='', device='cpu', file_in=None, waiting=True, silent=False):

    # Initialization
    result_ready = False
    if file_in is None:
        filepaths = None
    else:
        filepaths = [file_in]
    supported_ext = []
    for typ in supported:
        supported_ext.append(('all audio format', typ))

    if check_install(platform.system()) != 0:
        print(Colors.fg.red, 'Installation problems.   See suggestions a few lines above')
        # Ask for input to force hold to see stderr
        if silent is False:
            input('\nEnter anything to close window')
        return None, None

    # Request list of files in a browse dialog
    if filepaths is None:
        root = tk.Tk()
        root.withdraw()
        filepaths = filedialog.askopenfilenames(title='Please select files', filetypes=supported_ext)
        if filepaths is None or filepaths == '':
            print("No file chosen")
            if silent is False:
                input('\nEnter anything to close window')
            return None, None

    # Configuration for entire folder selection read with filepaths
    (config_path, config_basename, config_file_path, config) = configurator(filepaths[0])
    if model == '':
        model = config_section_map(config, "Whisper Preferences")['model']

    # Loop all selected files; use extensions to filter audio files
    txt_path = None
    for filepath in filepaths:
        (path, basename) = os.path.split(filepath)
        (file_root, extension) = os.path.splitext(basename)
        txt_path = os.path.join(path, file_root + '.txt')
        cache_path = os.path.expanduser('~') + '/.cache'  # Put cache in home so user needs it only once

        # Filter audio files; print message sometimes
        if screened(extension, filepath, txt_path, basename):
            continue

        # Transcribe an audio file
        command = 'whisper ' + filepath + ' --language en --output_format txt ' + '--fp16 False '
        if model != '':
            command += '--model ' + model
        start_time = timeit.default_timer()

        # Transcribe
        if silent is False:
            print(command + '\n')
            writer = get_writer('txt', path)
            wh_model = whisper.load_model(model, device=device, download_root=cache_path)
            print(Colors.bg.brightblack, Colors.fg.wheat)
            result = whisper.transcribe(wh_model, filepath, temperature=0.0, fp16=False, verbose=True)
            print(Colors.reset)
            print(command + '\n')
            if result == -1:
                print(Colors.fg.blue, 'failed...on to next file', Colors.reset)
                continue
            print(Colors.fg.orange, 'Transcribed in {:6.1f} seconds.'.format(timeit.default_timer() - start_time),
                  Colors.reset, end='')
            # Save the result in a text file and display it for pasting to writing documents
            #            writer and writer_args are defined in openai-whisper/transcribe.py
            writer_args = {'highlight_words': False, 'max_line_count': None, 'max_line_width': None}
            writer(result, txt_path, writer_args)
            result_ready = True
            print(Colors.fg.orange, "  The result is in ", Colors.fg.blue, txt_path, Colors.reset)
        else:
            writer = get_writer('txt', path)
            wh_model = whisper.load_model(model, device=device, download_root=cache_path)
            result = whisper.transcribe(wh_model, filepath, temperature=0.0, fp16=False, verbose=True)
            if result == -1:
                continue
            # Save the result in a text file and display it for pasting to writing documents
            #            writer and writer_args are defined in openai-whisper/transcribe.py
            writer_args = {'highlight_words': False, 'max_line_count': None, 'max_line_width': None}
            writer(result, txt_path, writer_args)
            result_ready = True

        print('')
        display_result(txt_path, platform.system(), silent)

        # Delay a little to allow windows to pop up without hiding each other.
        # The slower the computer, the more needed.
        time.sleep(1.0)

    # After all files are processed, ask for input to force hold to see stdout
    if waiting is True and silent is False:
        input('\nEnter anything to close window')

    return txt_path, result_ready


if __name__ == '__main__':
    def main(model=''):
        if model != '':
            print("user requested model '{:s}'".format(model))
        whisper_to_write(model=model)

    # Main call
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
