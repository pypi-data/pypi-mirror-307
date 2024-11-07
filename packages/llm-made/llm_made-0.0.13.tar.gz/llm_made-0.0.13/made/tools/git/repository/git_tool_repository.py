from abc import ABC, abstractmethod


class GitToolRepository(ABC):
    @staticmethod
    @abstractmethod
    def git_init():
        pass

    @staticmethod
    @abstractmethod
    def create_gitignore():
        pass

    @staticmethod
    @abstractmethod
    def git_commit():
        pass

    @staticmethod
    @abstractmethod
    def git_add():
        pass
