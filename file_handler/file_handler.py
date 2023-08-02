import glob
import os

from write_yaml import WriteYAML
from read_yaml import ReadFile


class FileHandler:
    def __init__(self, yaml_path: str, csv_file_path):
        self.added_files_list: list[str] = []
        self.all_files: list = []
        self.yaml_path = yaml_path
        self.csv_file_path = csv_file_path
        self.yaml_files_list: list[str] = []
        self.list_references: list[str] = []

    def list_files(self):
        self.all_files = os.listdir(self.yaml_path)
        self.yaml_files_list = glob.glob(self.yaml_path + "/*.yaml")
        self.write_all_files_names_to_yaml()

        for file in self.yaml_files_list:
            print(f"FileName: {file}")
            self.read_from_yaml(file)
            break

    def read_from_csv(self):
        self.csv_file_path = ""

    def write_to_yaml(self):
        csv_file = open(self.csv_file_path, 'a')
        csv_file.write("Test It")
        csv_file.write("Test It Again")

    def read_from_yaml(self, file_name):
        read_yaml = ReadFile(file_name)
        read_yaml.read_yaml()
        read_yaml.read()
        print(f"File Path Name: {file_name}")
        dict_list = read_yaml.get_references()
        self.list_references = list(dict_list.keys())
        dict_list = [{"file_name": file_name, "references": self.list_references}]
        writer = WriteYAML("../results/result.yaml")
        writer.write_to_yaml(dict_list)
        for ref in self.list_references:
            print(f"Unique Reference: {ref}")

    def write_all_files_names_to_yaml(self):
        print(f"All files: {self.all_files}")
        print(f"Directory: {self.yaml_files_list}")
        print(f"Count of files: {len(self.yaml_files_list)}")
        writer = WriteYAML("../results/files_added.yaml")
        writer.write_to_yaml(self.added_files_list)


def main():
    file_handler: FileHandler = FileHandler("../3gpp", "../results/result.yaml")
    file_handler.list_files()
    # file_handler.write_to_yaml()


if __name__ == "__main__":
    main()
