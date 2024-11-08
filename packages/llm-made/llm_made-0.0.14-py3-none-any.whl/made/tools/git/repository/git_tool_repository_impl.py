import os

from made.tools.git.repository.git_tool_repository import GitToolRepository
from made.tools.file.repository.file_tool_repository_impl import FileToolRepositoryImpl


class GitToolRepositoryImpl(GitToolRepository):
    @staticmethod
    def git_init(workspace_path: str):
        os.system(f"cd {workspace_path}; git init")

    @staticmethod
    def create_gitignore(workspace_path: str) -> None:
        FileToolRepositoryImpl.create_empty_file(
            os.path.join(workspace_path, ".gitignore")
        )

    @staticmethod
    def git_commit(workspace_path: str, message: str):
        os.system(f"cd {workspace_path}; git commit -m {message}")

    @staticmethod
    def git_add(workspace_path: str):
        os.system(f"cd {workspace_path}; git add .")
