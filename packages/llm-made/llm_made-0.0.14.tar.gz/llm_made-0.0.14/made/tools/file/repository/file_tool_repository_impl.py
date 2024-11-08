import os
import re
from typing import Dict

from made.tools.file.repository.file_tool_repository import FileToolRepository


class FileToolRepositoryImpl(FileToolRepository):
    @staticmethod
    def create_empty_file(file_path: str):
        with open(file_path, "w") as f:
            pass

    @staticmethod
    def read_file(file_path: str) -> str:
        with open(file_path, "r") as f:
            content = f.read()
        return content

    @staticmethod
    def write_file(file_path: str, content: str) -> None:
        with open(file_path, "w") as f:
            f.write(content)

    @staticmethod
    def update_file(file_path: str, content: str) -> None:
        with open(file_path, "a") as f:
            f.write(content)

    @staticmethod
    def delete_file(file_path) -> None:
        os.remove(file_path)

    @staticmethod
    def get_file_name_from_text(text: str, regex: str = r"(\w+\.\w+)"):
        for candidate in re.finditer(regex, text, re.DOTALL):
            file_name = candidate.group()
            file_name = file_name.lower()
        return file_name

    @staticmethod
    def abstract_contents_from_text(
        text: str, regex: str = r"\n(.+?)\n```.*?\n(.*?)```"
    ) -> Dict[str, str]:
        contents = {}
        matches = re.finditer(regex, text, re.DOTALL)
        for match in matches:
            file_name, content = match.groups()
            file_name = FileToolRepositoryImpl.get_file_name_from_text(file_name)
            contents[file_name] = content

        return contents

    @staticmethod
    def build_directory_structure(structure: Dict[str, str]):
        pass

    @staticmethod
    def convert_tree_structure_to_dict(tree_structure: str) -> Dict[str, str]:
        pass
