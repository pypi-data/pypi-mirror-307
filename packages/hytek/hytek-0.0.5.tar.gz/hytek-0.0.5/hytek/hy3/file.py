import zipfile
from logging import warning

from .records import Hy3Record, Hy3RecordGroup, RECORD_TYPES


__all__ = ("Hy3File",)


class Hy3File:
    def __init__(self, fp: str | None = None):
        self.records: list[Hy3Record] = []
        self.filepath: str | None = fp
        self.file = None

    def read_zip(self, fp: str, *, pwd: bytes | None = None) -> None:
        file = zipfile.ZipFile(fp)
        if self.filepath is None:
            for f in file.infolist():
                if f.filename.endswith(".hy3"):
                    if self.filepath is not None:
                        self.filepath = None
                        raise ValueError("Must specify .hy3 file name.")
                    self.filepath = f
            warning(f"Defaulting to first .hy3 file in zip: {fp}")
        if self.filepath is None:
            raise ValueError("No .hy3 file found in zip.")
        self.file = file.open(self.filepath, pwd=pwd)
        self.read()

    def read(self) -> None:
        if self.file is None:
            self.file = open(self.filepath, "rb")
        parents = []
        records = []
        data = self.file.read()
        for i, line in enumerate(data.splitlines()):
            record_type = line[:2].decode(errors="ignore")
            try:
                record = RECORD_TYPES.get(record_type, Hy3Record).parse_record(line)
            except Exception as e:
                raise Exception(f"Parsing failed for line {i + 1} type {record_type}: {e}") from e
            if type(record) is Hy3Record:
                warning(f"Unknown record type {record_type}")
                records.append(record)
                continue

            done = False
            while parents:
                parent = parents[-1]
                if parent._child_allowed(record):  # child record
                    parent.append_child(record)
                    parents.append(record)
                    done = True
                    break
                elif parent._group_allowed(record): # group record?
                    group = parent.add_to_group(record)
                    parents[-1] = group
                    # get the group's parent
                    # should be the record immediately before
                    # the group record
                    group_parent = parents[-2]
                    # update children of the group's parent
                    group_parent.children[-1] = group
                    done = True
                    break
                parents.pop()
            if not done:
                records.append(record)
                parents.append(record)
            pass

        self.records = records
        self.file.close()
        self.file = None

    def print_tree(self):
        for record in self.records:
            record.print_tree()

    def to_json(self) -> dict:
        return {"records": [record.to_json() for record in self.records]}