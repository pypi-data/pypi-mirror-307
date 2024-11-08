import os

from solidipes.loaders.file import File, load_file


class SymLink(File):
    """Symbolic link (special file)"""

    def __init__(self, **kwargs):
        from ..viewers.symlink import SymLink as SymLinkViewer

        super().__init__(**kwargs)
        self.compatible_viewers[:0] = [SymLinkViewer]  # TODO: to binary or file info

    # TODO: as sequence, if path does not exist, treat as separate file with some infos
    @File.loadable
    def linked_file(self):
        from pathlib import Path

        _path = str(Path(self.file_info.path).resolve())
        if os.path.exists(_path):
            return load_file(_path)

        return _path

    def _valid_loading(self):
        return self.linked_file._valid_loading()
