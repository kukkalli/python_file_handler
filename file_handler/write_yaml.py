from typing import TextIO

import yaml


class WriteYAML:

    def __init__(self, file_name):
        self.file: TextIO = TextIO()
        self.file_name = file_name

    def write(self):
        self.file = open(self.file_name, 'r')
        print(f"Existing File Data: {self.file}")
        self.file.close()

    def write_to_yaml(self, dict_object):
        with open(self.file_name, 'a') as f:
            data = yaml.dump(dict_object, f, sort_keys=False, default_flow_style=False)
            print(f"Data dumped: {data}")
