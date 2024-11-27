#  install.py
#  2024-Apr-13  Dave Gutz   Create
# Copyright (C) 2024 Dave Gutz
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
from whisper_util import run_shell_cmd
from Colors import Colors
import os
import shutil

# Provide dependencies
speak_write_icons_path = None
speak_write_icons_dest_path = None
fwg_path = None
fwg_dest_path = None

# Create executable
if sys.platform == 'win32':
    test_cmd_copy = None
    speak_write_icons_path = os.path.join(os.getcwd(), 'speak_write.png')
    speak_write_icons_dest_path = os.path.join(os.getcwd(), 'dist', 'gui_speak_write',  '_internal', 'speak_write.png')
    fwg_path = os.path.join(os.getcwd(), 'fwg.png')
    fwg_dest_path = os.path.join(os.getcwd(), 'dist', 'gui_speak_write', '_internal', 'fwg.png')
    test_cmd_create = 'pyinstaller .\\gui_speak_write.py --recursive-copy-metadata "openai-whisper" --recursive-copy-metadata "ffmpeg-python"  --recursive-copy-metadata "pyaudio" --i speak_write.ico -y'
    result = run_shell_cmd(test_cmd_create, silent=False)
    if result == -1:
        print(Colors.fg.red, 'failed', Colors.reset)
        exit(1)
    else:
        print(Colors.fg.green, 'success', Colors.reset)

    # Hand-fix pyinstaller for pvrecorder
    pvr_path = os.path.join(os.getcwd(), 'venv', 'Lib', 'site-packages', 'pvrecorder')
    pvr_dest_path = os.path.join(os.getcwd(), 'dist', 'gui_speak_write', '_internal', 'pvrecorder')
    shutil.copytree(pvr_path, pvr_dest_path)
    shutil.copystat(pvr_path, pvr_dest_path)
    print(Colors.fg.green, "copied pvrecorder", Colors.reset)

    # Hand-fix pyinstaller for whisper
    whi_path = os.path.join(os.getcwd(), 'venv', 'Lib', 'site-packages', 'whisper')
    whi_dest_path = os.path.join(os.getcwd(), 'dist', 'gui_speak_write', '_internal', 'whisper')
    shutil.copytree(whi_path, whi_dest_path)
    shutil.copystat(whi_path, whi_dest_path)
    print(Colors.fg.green, "copied whisper", Colors.reset)

    shutil.copyfile(speak_write_icons_path, speak_write_icons_dest_path)
    shutil.copystat(speak_write_icons_path, speak_write_icons_dest_path)
    shutil.copyfile(fwg_path, fwg_dest_path)
    shutil.copystat(fwg_path, fwg_dest_path)
    print(Colors.fg.green, "copied icon files", Colors.reset)

# Install as deeply as possible
test_cmd_install = None

# Install
login = os.getlogin()
if sys.platform == 'linux':
    desktop_entry = f"""[Desktop Entry]
Name=gui_speak_write
Path=/home/{login}/Documents/Recordings
Icon=/home/{login}/Documents/GitHub/fwgWhisper/speak_write.ico
comment=app
Encoding=UTF-8
Categories=Utility
Exec=/home/{login}/Documents/GitHub/fwgWhisper/venv/bin/python3 /home/{login}/Documents/GitHub/fwgWhisper/GUI_Speak_Write.py
Terminal=true
Type=Application
"""
    with open(f"/home/{login}/Desktop/GUI_Speak_Write.desktop", "w") as text_file:
        result = text_file.write("%s" % desktop_entry)
    if result == -1:
        print(Colors.fg.red, 'failed', Colors.reset)
    else:
        print(Colors.fg.green, 'success', Colors.reset)

    #  Launch permission
    test_cmd_launch = f'gio set /home/{login}/Desktop/GUI_Speak_Write.desktop metadata::trusted true'
    result = run_shell_cmd(test_cmd_launch, silent=False)
    if result == -1:
        print(Colors.fg.red, 'gio set failed', Colors.reset)
    else:
        print(Colors.fg.green, 'gio set success', Colors.reset)
    test_cmd_perm = 'chmod a+x ~/Desktop/GUI_Speak_Write.desktop'
    result = run_shell_cmd(test_cmd_perm, silent=False)
    if result == -1:
        print(Colors.fg.red, 'failed', Colors.reset)
    else:
        print(Colors.fg.green, 'success', Colors.reset)

    # Execute permission
    test_cmd_perm = 'chmod a+x ~/Desktop/GUI_Speak_Write.desktop'
    result = run_shell_cmd(test_cmd_perm, silent=False)
    if result != 0:
        print(Colors.fg.red, f"'chmod ...' failed code {result}", Colors.reset)
    else:
        print(Colors.fg.green, 'chmod success', Colors.reset)

    # Move file
    try:
        result = shutil.move(f'/home/{login}/Desktop/GUI_Speak_Write.desktop',
                             '/usr/share/applications/GUI_Speak_Write.desktop')
    except PermissionError:
        print(Colors.fg.red,
              f"Stop and establish sudo permissions", f"  or\n"
              f"sudo mv /home/{login}/Desktop/GUI_Speak_Write.desktop /usr/share/applications",
              Colors.reset)
        exit(1)
    if result != '/usr/share/applications/GUI_Speak_Write.desktop':
        print(Colors.fg.red, f"'mv ...' failed code {result}", Colors.reset)
    else:
        print(Colors.fg.green,
              'mv success.  Browse apps :: and make it favorites.  Open and set desired path to Recordings\n'
              "you shouldn't have to remake shortcuts",
              Colors.reset)
elif sys.platform == 'darwin':
    print(Colors.fg.green,
          f"Make sure 'Python Launcher' (Python Script Preferences) option for 'Allow override with #! in script' is checked.\n"
          f"in Finder double-click on 'speak_write.png'.  Edit-copy the image\n"
          f"in Finder ctrl-click on 'GUI_Speak_Write.py'\n"
          f"   - 'Get Info', click on 2nd icon, paste.   Drag item to taskbar.",
          Colors.reset)
else:
    print(Colors.fg.green,
          f"Browse to ./dist/GUI_Speak_Write and double-click.  Create shortcut first time and move to desktop.\n"
          f"double-click on  'GUI_Speak_Write.exe - Shortcut', browse it's settings to desired Recordings folder, pin to taskbar\n"
          f"in shortcut properties, make sure 'Start in:' is this folder where this script resides\n"
          "you shouldn't have to remake shortcuts",
          Colors.reset)
