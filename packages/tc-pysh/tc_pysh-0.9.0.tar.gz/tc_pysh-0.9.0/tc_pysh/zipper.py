import zipfile as z
import tarfile as tar

from typing import Callable, Optional, Union

from .path import AbsolutePath, Path


ArFile = Union[z.ZipFile, tar.TarFile]
AbsolutePathTransform = Callable[[AbsolutePath], Path]


class Zipper:
    "Multi format compressor (you should rather be using tc_pysh.utils.archive)."

    def __init__(self, format: str):
        self.format = format

    def open(self, path: AbsolutePath) -> "Archive":
        return Archive(path, self)

    def exists(self, path: AbsolutePath) -> bool:
        if self.format in {"zip", "ZIP"}:
            return z.is_zipfile(path.to_str())
        elif self.format in {"tgz", "tar.gz"}:
            return tar.is_tarfile(path.to_str())
        elif self.format in {"txz", "tar.xz"}:
            return tar.is_tarfile(path.to_str())
        else:
            raise NotImplementedError("Unknown format")

    def _open(self, path: AbsolutePath) -> ArFile:
        if self.format in {"zip", "ZIP"}:
            return z.ZipFile(path.to_str(), "w")
        elif self.format in {"tgz", "tar.gz"}:
            return tar.open(path.to_str(), "w:gz")
        elif self.format in {"txz", "tar.xz"}:
            return tar.open(path.to_str(), "w:xz")
        else:
            raise NotImplementedError("Unknown format")

    def add(
        self,
        path: AbsolutePath,
        target: ArFile,
        transform: Union[AbsolutePathTransform, None, str] = None,
    ) -> None:
        if isinstance(transform, str):
            arcname: Optional[str] = transform
        elif transform is not None:
            arcname = transform(path).to_str()
        else:
            arcname = None
        if arcname == "":
            arcname = "."
        if isinstance(target, z.ZipFile):
            target.write(path.to_str(), arcname=arcname)
        elif isinstance(target, tar.TarFile):
            target.add(path.to_str(), arcname=arcname)


class Archive:
    def __init__(self, path: AbsolutePath, zipper: Zipper):
        self.path = path
        self.zipper = zipper
        if path.exists():
            raise ValueError("File already exists. Append mode is not supported.")
        self.file: ArFile = zipper._open(path)
        self.default_transform: Union[AbsolutePathTransform, None, str] = None

    def use_transform(self, transform: AbsolutePathTransform):
        self.default_transform = transform

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def add(
        self,
        path: AbsolutePath,
        transform: Union[AbsolutePathTransform, None, str] = None,
    ):

        if transform is None and self.default_transform is not None:
            transform = self.default_transform

        self.zipper.add(path, self.file, transform=transform)

    def close(self):
        self.file.close()
