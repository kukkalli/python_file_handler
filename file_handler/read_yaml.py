from typing import TextIO, AnyStr

import yaml
from yaml.loader import SafeLoader


class ReadFile:

    def __init__(self, file_name):
        self.absolute_file_name = file_name
        self.data = None
        self.file: TextIO = TextIO()
        self.title: str = ""
        self.description: str = ""
        self.description2: str = ""
        self.url = ""
        self.references_list: dict[str, str] = {}

    def read_yaml(self):
        with open(self.absolute_file_name, 'r') as f:
            self.data = yaml.load(f, Loader=SafeLoader)
            # print(data)
            self.set_info()
            self.set_external_docs()
            self.set_other()

    def read(self):
        self.file = open(self.absolute_file_name, 'r')

    def set_info(self):
        self.title = self.data['info']['title']
        self.description = self.data['info']['description']

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def set_external_docs(self):
        # print(f"ExternalDocs: {self.data['externalDocs']}")
        self.description2 = self.data['externalDocs']['description']
        self.url = self.data['externalDocs']['url']

    def get_description2(self):
        return self.description2

    def get_url(self):
        return self.url

    def set_other(self):
        for token in self.data:
            print(token)

    def get_references(self) -> dict[str, str]:
        lines: list[AnyStr] = self.file.readlines()
        for line in lines:
            if line.find("$ref: 'TS") != -1:
                # count = line.find("$ref: 'TS")
                # print(f"Count: {count}")
                count_start = line.find("TS")
                # print(f"Count Start: {count_start}")
                count_end = line.find(".yaml#") + 5
                # print(f"Count End: {count_end}")
                # print(f"Line: {line}")
                # print(f"file name: {line[count_start:count_end]}")
                file_name = line[count_start:count_end]
                self.references_list[file_name] = file_name
        return self.references_list
