from abc import ABC, abstractmethod


class DockerToolRepository(ABC):
    @staticmethod
    @abstractmethod
    def get_client():
        pass

    @staticmethod
    @abstractmethod
    def pull_image():
        pass

    @staticmethod
    @abstractmethod
    def start_container():
        pass

    @staticmethod
    @abstractmethod
    def stop_container():
        pass

    @staticmethod
    @abstractmethod
    def get_container():
        pass

    @staticmethod
    @abstractmethod
    def exec_command():
        pass
