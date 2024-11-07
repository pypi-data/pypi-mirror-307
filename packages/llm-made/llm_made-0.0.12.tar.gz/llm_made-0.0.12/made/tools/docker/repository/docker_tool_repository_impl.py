import os
import time
from typing import Optional

import docker
from docker import DockerClient
from docker.models.containers import Container

from made.tools.docker.repository.docker_tool_repository import DockerToolRepository


class DockerToolRepositoryImpl(DockerToolRepository):
    @staticmethod
    def get_client() -> DockerClient:
        return docker.from_env()

    @staticmethod
    def pull_image(client: DockerClient, image_name: str = "python:3.9-slim"):
        repository, tag = image_name.split(":")
        client.images.pull(repository, tag)

    @staticmethod
    def start_container(container: Container):
        container.start()

    @staticmethod
    def stop_container(container: Container):
        container.stop()

    @staticmethod
    def get_container(
        container_name: str,
        image_name: Optional[str] = "python:3.9-slim",
        port: Optional[int] = 7979,
        volume: Optional[str] = "project_zoo",
        wait_delay: Optional[int] = 3,
    ) -> Container:
        client = DockerToolRepositoryImpl.get_client()
        containers = [container.name for container in client.containers.list(all=True)]
        if container_name in containers:
            container = client.containers.get(container_name)
            if container.status != "running":
                DockerToolRepositoryImpl.start_container(container)
        else:
            images = [image.attrs["RepoTags"] for image in client.images.list(all=True)]
            if image_name not in images:
                DockerToolRepositoryImpl.pull_image(client, image_name)

            image = client.images.get(image_name)
            container = client.containers.run(
                image=image,
                name=container_name,
                detach=True,
                tty=True,
                ports={f"{port}/tcp": port},
                volumes={os.path.abspath(volume): {"bind": f"/{volume}", "mode": "rw"}},
            )
        time.sleep(wait_delay)

        if not container:
            raise RuntimeError(f"Failed to create and start `{container_name}`")

        return container

    @staticmethod
    def exec_command(container: Container, command: str):
        res = container.exec_run(command)
        exit_code = res.exit_code
        output = res.output.decode()

        return output, exit_code
