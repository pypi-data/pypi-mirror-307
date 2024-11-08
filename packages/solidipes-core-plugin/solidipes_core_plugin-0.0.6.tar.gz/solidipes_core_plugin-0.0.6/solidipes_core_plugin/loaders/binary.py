from datasize import DataSize
from solidipes.loaders.file import File


class Binary(File):
    """File of unsupported type"""

    def __init__(self, **kwargs):
        from ..viewers.binary import Binary as BinaryViewer

        super().__init__(**kwargs)
        self.add("metadata")
        self.compatible_viewers[:0] = [BinaryViewer]

    @File.cached_property
    def text(self):
        text = ""
        if self.file_info.type is not None:
            text += f"File type: {self.file_info.type}\n"

        text += f"File size: {DataSize(self.file_info.size):.2a}"
        return text

    def _valid_extension(self):
        import os

        self.errors.append(
            f"Unknown filetype '{self.file_info.type}' with extension '{os.path.splitext(self.file_info.path)[1]}'"
        )
        return False
