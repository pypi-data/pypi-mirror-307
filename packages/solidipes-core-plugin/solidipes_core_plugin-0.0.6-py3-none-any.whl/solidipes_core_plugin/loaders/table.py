import pandas as pd
from solidipes.loaders.file import File


class Table(File):
    """Table file loaded with Pandas"""

    supported_mime_types = {
        "text/csv": "csv",
        "application/vnd.ms-excel": "xlsx",
        "application/numpy/array": "npy",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
    }

    def __init__(self, **kwargs):
        from ..viewers.table import Table as TableViewer

        super().__init__(**kwargs)

        path = kwargs["path"]

        # find loader matching file extension
        if self.file_info.type == "text/csv":
            self.pandas_loader = self.read_csv
        elif self.file_info.type == "application/vnd.ms-excel" or self.file_info.extension in ["xlsx"]:
            self.pandas_loader = pd.read_excel
        elif self.file_info.type.startswith("application/numpy"):
            self.pandas_loader = self.read_numpy
        else:
            raise RuntimeError(f"File type not supported: {path} {self.file_info.type}")

        self.compatible_viewers[:0] = [TableViewer]

    def read_csv(self, fname, **kwargs):
        import csv

        with open(fname) as fp:
            sep = csv.Sniffer().sniff(fp.readline()).delimiter
            ret = pd.read_csv(fname, sep=sep, **kwargs)
            return ret

    def read_numpy(self, fname, **kwargs):
        import numpy

        f = numpy.load(fname)
        f = pd.DataFrame(f)
        return f

    def validate_header(self, header):
        for h in header:
            try:
                h = float(h)
                self.errors.append(f"Incorrect header: {header}")
                break
            except Exception:
                pass
            if h.startswith("Unnamed"):
                self.errors.append(f"Incorrect header: {header}")
                break

    @File.loadable
    def header(self):
        data = self.pandas_loader(self.file_info.path, nrows=0)
        header = list(data.columns)
        self.validate_header(header)
        return ", ".join(header)

    @File.loadable
    def table(self):
        return self.pandas_loader(self.file_info.path)
