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

test_cmd_create = None
test_cmd_copy = None
popcorn_path = os.path.join(os.getcwd(), 'speak_write.png')
popcorn_dest_path = os.path.join(os.getcwd(), 'dist', 'speak_write', 'speak_write.png')

# Create executable
if sys.platform == 'linux':
    test_cmd_create = "pyinstaller ./speak_write.py --hidden-import='PIL._tkinter_finder' --icon='speak_write.ico' -y"
elif sys.platform == 'darwin':
    print("simplified...wait for green comments")
else:
    test_cmd_create = 'pyinstaller .\\speak_write.py --i speak_write.ico -y'

if sys.platform != 'darwin':
    result = run_shell_cmd(test_cmd_create, silent=False)
    if result == -1:
        print(Colors.fg.red, 'failed', Colors.reset)
        exit(1)
    else:
        print(Colors.fg.green, 'success', Colors.reset)

    # Provide dependencies
    shutil.copyfile(popcorn_path, popcorn_dest_path)
    shutil.copystat(popcorn_path, popcorn_dest_path)
    print(Colors.fg.green, "copied files", Colors.reset)

# Install as deeply as possible
test_cmd_install = None
if sys.platform == 'linux':

    # Install
    desktop_entry = """[Desktop Entry]
Name=speak_write
Exec=/home/daveg/Documents/GitHub/fwgWhisper/dist/speak_write/speak_write
Path=/home/daveg/Documents/GitHub/fwgWhisper/dist/speak_write
Icon=/home/daveg/Documents/GitHub/fwgWhisper/speak_write.ico
comment=app
Type=Application
Terminal=true
Encoding=UTF-8
Categories=Utility
"""
    with open("/home/daveg/Desktop/speak_write.desktop", "w") as text_file:
        result = text_file.write("%s" % desktop_entry)
    if result == -1:
        print(Colors.fg.red, 'failed', Colors.reset)
    else:
        print(Colors.fg.green, 'success', Colors.reset)

    #  Launch permission
    test_cmd_launch = 'gio set /home/daveg/Desktop/speak_write.desktop metadata::trusted true'
    result = run_shell_cmd(test_cmd_launch, silent=False)
    if result == -1:
        print(Colors.fg.red, 'gio set failed', Colors.reset)
    else:
        print(Colors.fg.green, 'gio set success', Colors.reset)
    test_cmd_perm = 'chmod a+x ~/Desktop/speak_write.desktop'
    result = run_shell_cmd(test_cmd_perm, silent=False)
    if result == -1:
        print(Colors.fg.red, 'failed', Colors.reset)
    else:
        print(Colors.fg.green, 'success', Colors.reset)

    # Execute permission
    test_cmd_perm = 'chmod a+x ~/Desktop/speak_write.desktop'
    result = run_shell_cmd(test_cmd_perm, silent=False)
    if result != 0:
        print(Colors.fg.red, f"'chmod ...' failed code {result}", Colors.reset)
    else:
        print(Colors.fg.green, 'chmod success', Colors.reset)

    # Move file
    try:
        result = shutil.move('/home/daveg/Desktop/speak_write.desktop',
                             '/usr/share/applications/speak_write.desktop')
    except PermissionError:
        print(Colors.fg.red, f"Stop and establish sudo permissions", Colors.reset)
        print(Colors.fg.red, f"  or", Colors.reset)
        print(Colors.fg.red, f"sudo mv /home/daveg/Desktop/speak_write.desktop /usr/share/applications/.",
              Colors.reset)
        exit(1)
    if result != '/usr/share/applications/speak_write.desktop':
        print(Colors.fg.red, f"'mv ...' failed code {result}", Colors.reset)
    else:
        print(Colors.fg.green, 'mv success.  Browse apps :: and make it favorites.  Open and set path to dataReduction',
              Colors.reset)
        print(Colors.fg.green, "you shouldn't have to remake shortcuts", Colors.reset)
elif sys.platform == 'darwin':
    print(f"macOS: in Finder ctrl-click on 'speak_write.py' select 'duplicate.'"
          f" Open and copy icon into paste buffer."
          f" Then 'Get Info' on the duplicate, click on 2nd icon, paste.   Drag duplicate item to taskbar.")
else:
    print(Colors.fg.green, f"double-click on  'speak_write.exe - Shortcut', browse to DB folder, pin to taskbar",
          Colors.reset)
    print(Colors.fg.green, "you shouldn't have to remake shortcuts", Colors.reset)
