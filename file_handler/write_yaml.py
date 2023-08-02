from typing import TextIO

import yaml


class WriteFile:

    def __init__(self, file_name):
        self.file: TextIO = TextIO()
        self.file_name = file_name

    def write(self):
        self.file = open(self.file_name, 'a')
        print(f"Existing File Data: {self.file}")
        self.file.close()

    def write_to_yaml(self, dict_object: list, overwrite: False):

        if overwrite:
            overwrite = 'w'
        else:
            overwrite = "a"
        with open(self.file_name, overwrite) as f:
            yaml.dump(dict_object, f, sort_keys=True, default_flow_style=False)
