import glob

from read_yaml import ReadFile
from write_yaml import WriteFile


class FileHandler:
    def __init__(self, yaml_path: str, result_file_path: str):
        self.yaml_path = yaml_path
        self.result_file_path: str = result_file_path

        self.added_files_list: list[str] = []
        self.added_files_dict: dict[str, str] = {}
        self.missing_files_list: list[str] = []
        self.missing_files_dict: dict[str, str] = {}
        self.openapi_list: list[dict] = []
        self.openapi_dict: dict[str, dict] = {}

        self.yaml_files_list: list[str] = []

        self.list_references: list[str] = []
        self.dict_references: dict[str, str] = {}

    def list_files(self):
        self.yaml_files_list = glob.glob(self.yaml_path + "*.yaml")
        self.yaml_files_list.sort()

    def read_files_added_list(self):
        read_files_added_list = ReadFile(self.result_file_path + "files_added.yaml")
        files_added = read_files_added_list.read_yaml()
        for file_added in files_added:
            self.added_files_dict[file_added] = file_added

    def read_openapi_list(self):
        read_openapi_list = ReadFile(self.result_file_path + "complete_openapi.yaml")
        complete_openapi = read_openapi_list.read_yaml()
        for openapi in complete_openapi:
            # print(f"Added file in openapi: {openapi['file_name']}")
            self.openapi_dict[openapi["file_name"]] = openapi

    def read_missing_openapi(self):
        read_missing_openapi = ReadFile(self.result_file_path + "missing_openapi.yaml")
        missing_openapi = read_missing_openapi.read_yaml()
        for openapi in missing_openapi:
            self.missing_files_dict[openapi] = openapi

    def find_references(self):
        index_length = len(self.yaml_path)
        i = 0
        for file in self.yaml_files_list:
            file_name = file[index_length:]
            if file_name not in self.added_files_dict:
                self.added_files_dict[file_name] = file_name
                self.read_from_yaml(file, file_name)

    def read_from_yaml(self, file, file_name):
        read_yaml = ReadFile(file)
        read_yaml.read_openapi_yaml()
        dict_list = read_yaml.get_references()
        list_ref = list(dict_list.keys())
        list_ref.sort()
        self.dict_references = self.dict_references | dict_list
        self.list_references = list(self.dict_references.keys())
        self.list_references.sort()
        object_dict = {"file_name": file_name,
                       "title": read_yaml.get_title(),
                       "url": read_yaml.get_url(),
                       "description": read_yaml.get_description(),
                       "description2": read_yaml.get_description2(),
                       "references": list_ref}
        self.openapi_list.append(object_dict)

    def write_files_added(self):
        self.added_files_list = list(self.added_files_dict.keys())
        self.added_files_list.sort()
        writer = WriteFile(self.result_file_path + "files_added.yaml")
        writer.write_to_yaml(self.added_files_list, True)

    def write_openapi_files(self):
        writer = WriteFile(self.result_file_path + "complete_openapi.yaml")
        writer.write_to_yaml(self.openapi_list, True)

    def write_missing_files_names_to_yaml(self):
        references_list = list(self.dict_references.keys())
        for reference_file in references_list:
            if reference_file not in self.added_files_dict:
                self.missing_files_list.append(reference_file)
        self.missing_files_list.sort()
        writer = WriteFile(self.result_file_path + "missing_openapi.yaml")
        writer.write_to_yaml(self.missing_files_list, True)

    def check_completeness(self):
        self.read_files_added_list()
        self.read_openapi_list()
        self.read_missing_openapi()

        self.list_files()

        self.find_references()
        self.write_files_added()
        self.write_openapi_files()
        self.write_missing_files_names_to_yaml()


def main():
    file_handler: FileHandler = FileHandler("../3gpp/", "../results/")
    file_handler.check_completeness()


if __name__ == "__main__":
    main()
