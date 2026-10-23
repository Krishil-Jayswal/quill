from abc import ABC, abstractmethod

class StorageBackend(ABC):
    @abstractmethod
    def upload_file(
        self,
        local_path: str,
        object_key: str
    ) -> None:
        ...

    @abstractmethod
    def upload_directory(
        self,
        local_dir: str,
        object_prefix: str
    ) -> None:
        ...

    @abstractmethod
    def download_file(
        self,
        object_key: str,
        local_path: str
    ) -> None:
        ...

    @abstractmethod
    def download_files(
        self,
        object_keys: list[str],
        local_dir: str
    ) -> None:
        ...

    @abstractmethod
    def download_folder(
        self,
        object_prefix: str,
        local_path: str
    ) -> None:
        ...

    @abstractmethod
    def exists(
        self,
        object_key: str
    ) -> bool:
        ...

    @abstractmethod
    def delete(
        self,
        object_key: str
    ) -> None:
        ...