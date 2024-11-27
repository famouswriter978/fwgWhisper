# Begini - configuration class using .ini files
#  2024-Nov-04  Dave Gutz   Create
# Copyright (C) 2024 Dave Gutz and Sarah E. Gutz
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
from configparser import ConfigParser
import os
import platform

class Begini(ConfigParser):

    def __init__(self, name, def_dict_):
        ConfigParser.__init__(self)

        (config_path, config_basename) = os.path.split(name)
        if platform.system() == 'Linux':
            self.username = os.getlogin()
            config_txt = os.path.splitext(config_basename)[0] + '_linux.ini'
            self.config_file_path = os.path.join('/home', self.username, '.local', config_txt)
        elif platform.system() == 'Darwin':
            self.username = os.path.expanduser('~')
            config_txt = os.path.splitext(config_basename)[0] + '_macos.ini'
            self.config_file_path = os.path.join(self.username, '.local/', config_txt)
        else:
            config_txt = os.path.splitext(config_basename)[0] + '.ini'
            self.config_file_path = os.path.join(os.getenv('LOCALAPPDATA'), config_txt)
        print('config file', self.config_file_path)
        if os.path.isfile(self.config_file_path):
            self.read(self.config_file_path)
        else:
            with open(self.config_file_path, 'w') as cfg_file:
                self.read_dict(def_dict_)
                self.write(cfg_file)
            print('wrote', self.config_file_path)

    # Get an item
    def get_item(self, ind, item):
        return self[ind][item]

    # Put an item
    def put_item(self, ind, item, value):
        self[ind][item] = value
        self.save_to_file()

    # Save again
    def save_to_file(self):
        with open(self.config_file_path, 'w') as cfg_file:
            self.write(cfg_file)
        print('wrote', self.config_file_path)

