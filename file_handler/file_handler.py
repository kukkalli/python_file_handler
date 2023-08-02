import glob
import os

from write_yaml import WriteFile
from read_yaml import ReadFile


class FileHandler:
    def __init__(self, yaml_path: str, result_file_path):
        self.added_files_dict: dict[str, str] = {}
        self.added_files_list: list[str] = []
        self.all_files: list = []
        self.result_file_path = result_file_path
        self.yaml_path = yaml_path
        self.yaml_files_list: list[str] = []
        self.list_references: list[str] = []
        self.dict_references: dict[str, str] = {}

    def list_files(self):
        self.all_files = os.listdir(self.yaml_path)
        self.yaml_files_list = glob.glob(self.yaml_path + "*.yaml")

    def read_files_added_list(self):
        read_files_added_list = ReadFile(self.result_file_path+"files_added.yaml")
        files_added = read_files_added_list.read_yaml()
        for file_added in files_added:
            self.added_files_dict[file_added] = files_added

    def find_references(self):
        index_length = len(self.yaml_path)
        print(f"path length: {index_length}")
        i = 0
        for file in self.yaml_files_list:
            file_name = file[index_length:]
            # print(f"file_name {file_name} exists: {file_name in self.added_files_dict}")
            if file_name not in self.added_files_dict:
                self.added_files_dict[file_name] = file_name
                self.read_from_yaml(file, file_name)
                print(f"file_name {file_name} exists: {file_name in self.added_files_dict}")
            i = i + 1
            if i > 4:
                break

    def write_to_yaml(self):
        csv_file = open(self.result_file_path, 'a')
        csv_file.write("Test It")
        csv_file.write("Test It Again")
        csv_file.close()

    def read_from_yaml(self, file, file_name):
        read_yaml = ReadFile(file)
        read_yaml.read_yaml()
        print(f"File Path Name: {file}")
        dict_list = read_yaml.get_references()
        print(f"Dictionary returned: {dict_list}")
        list_ref = list(dict_list.keys())
        list_ref.sort()
        self.dict_references = self.dict_references | dict_list
        self.list_references = list(self.dict_references.keys())
        self.list_references.sort()
        print(f"Dictionary: {self.dict_references}, list_ref: {list_ref}")
        dict_list = [{"file_name": file_name, "references": list_ref}]
        writer = WriteFile(self.result_file_path + "complete_openapi.yaml")
        writer.write_to_yaml(dict_list, False)
        for ref in self.list_references:
            print(f"Unique Reference: {ref}")

    def write_all_files_names_to_yaml(self):
        print(f"All files: {self.all_files}")
        print(f"Directory: {self.yaml_files_list}")
        print(f"Count of files: {len(self.yaml_files_list)}")
        writer = WriteFile("../results/files_added.yaml")
        writer.write_to_yaml(self.added_files_list, True)

    def write_to_files_added(self):
        self.added_files_list = list(self.added_files_dict.keys())
        self.added_files_list.sort()
        writer = WriteFile("../results/files_added.yaml")
        writer.write_to_yaml(self.added_files_list, True)

    def check_completeness(self):
        self.read_files_added_list()
        self.list_files()
        self.find_references()
        self.write_to_files_added()


def main():
    file_handler: FileHandler = FileHandler("../3gpp/", "../results/")
    file_handler.check_completeness()
    # file_handler.write_to_yaml()


if __name__ == "__main__":
    main()
