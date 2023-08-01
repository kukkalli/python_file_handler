import glob
import os

from read_yaml import ReadYAML


class FileHandler:
    def __init__(self, yaml_path: str, csv_file_path):
        self.all_files: list = []
        self.yaml_path = yaml_path
        self.csv_file_path = csv_file_path
        self.yaml_files_list: list[str] = []
        self.list_references: list[str] = []

    def list_files(self):
        self.all_files = os.listdir(self.yaml_path)
        print(f"All files: {self.all_files}")
        self.yaml_files_list = glob.glob(self.yaml_path + "/*.yaml")

        print(f"Directory: {self.yaml_files_list}")

        for file in self.yaml_files_list:
            print(f"FileName: {file}")
            self.read_from_yaml(file)

    def read_from_csv(self):
        self.csv_file_path = ""

    def write_to_csv(self):
        csv_file = open(self.csv_file_path, 'w')

        csv_file.write("Test It")
        csv_file.write("Test It Again")

    def read_from_yaml(self, file_name):
        read_yaml = ReadYAML(file_name)
        read_yaml.read()
        print(f"File Path Name: {file_name}")
        dict_list = read_yaml.get_other_references()
        self.list_references = list(dict_list.keys())
        for ref in self.list_references:
            print(f"Unique Reference: {ref}")


def main():
    file_handler: FileHandler = FileHandler("../3gpp", "../csv/result.csv")
    file_handler.list_files()
    file_handler.write_to_csv()

    # writing to file
    file1 = open('myfile.txt', 'w')
    file1.writelines(L)
    file1.close()


if __name__ == "__main__":
    main()
