from __future__ import annotations

import math
import datetime
from typing import Any, Callable, Self, Type

from .converters import date, time


__all__ = (
    "Field",
    "Hy3RecordGroup",
    "Hy3Record",
    "Hy3A1Record",
    "Hy3B1Record",
    "Hy3B2Record",
    "Hy3C1Record",
    "Hy3C2Record",
    "Hy3C3Record",
    "Hy3D1Record",
    "Hy3E1Record",
    "Hy3E2Record",
    "Hy3F1Record",
    "Hy3F2Record",
    "Hy3F3Record",
    "Hy3G1Record",
    "Hy3H1Record",
    "Hy3H2Record",
    "RECORD_TYPES"
)


ALLOWED_CHILDREN = {
    "A": ["B"],
    "B": ["C"],
    "C": ["D", "F"],
    "D": ["E"],
    "E": ["G", "H"],
    "F": ["G", "H"],
}


class Field:
    def __init__(self, *, name: str, length: int, type: Callable[[str], Any] = str):
        self.name = name
        self.length = length
        self.type = type


class Hy3RecordGroup:
    def __init__(self, *records: Type[Hy3Record]):
        self.group_type = records[0].record_type[0]
        self.records = list(records)
        self.children = []

    def __repr__(self):
        return f"<Hy3RecordGroup group_type={self.group_type} records={self.records}>"

    def _child_allowed(self, child: Hy3Record | Hy3RecordGroup) -> bool:
        return child.record_type[0] in ALLOWED_CHILDREN.get(self.record_type[0], [])

    def append_child(self, child: Hy3Record | Hy3RecordGroup) -> None:
        if not self._child_allowed(child):
            raise Exception("Child record type is not allowed in this parent.")
        self.children.append(child)

    def remove_child(self, child: Hy3Record | Hy3RecordGroup) -> None:
        self.children.remove(child)

    def pop_child(self, index: int) -> Hy3Record | Hy3RecordGroup:
        return self.children.pop(index)

    def print_tree(self, depth: int = 0) -> None:
        print("  " * depth + str(self))
        for child in self.children:
            child.print_tree(depth + 1)

    def to_json(self) -> dict:
        return {
            "type": "group",
            "group_type": self.group_type,
            "records": [record.to_json() for record in self.records],
            "children": [child.to_json() for child in self.children]
        }

    @property
    def record_type(self) -> str:
        return self.records[-1].record_type

    def _group_allowed(self, record: Type[Hy3Record]) -> bool:
        if record.record_type[0] != self.group_type:
            return False
        if int(record.record_type[1]) <= int(self.records[-1].record_type[1]):
            return False
        return True

    def add_to_group(self, record: Type[Hy3Record]) -> Self:
        if not self._group_allowed(record):
            raise Exception("Cannot group records")
        self.records.append(record)
        return self

    def to_line(self) -> bytes:
        result = b""
        for record in self.records:
            result += record.to_line() + b"\n"
        return result


class Hy3Record:
    record_type: str
    fields: list[Field]
    data: dict[str, Any]
    raw: bytes
    children: list[Type[Hy3Record | Hy3RecordGroup]] = []

    def __init__(self, raw: bytes = b"", /, **kwargs):
        self.data: dict[str, Any] = kwargs
        self.raw: bytes = raw
        self.children: list[Type['Hy3Record']] = []

    def __repr__(self):
        return f"<{self.__class__.__name__} children={self.children}>"

    def __getitem__(self, item: str) -> Any:
        return self.data[item]

    def __setitem__(self, item: str, value: Any) -> None:
        self.data[item] = value

    def _child_allowed(self, child: Type[Hy3Record | Hy3RecordGroup]) -> bool:
        return child.record_type[0] in ALLOWED_CHILDREN.get(self.record_type[0], [])

    def append_child(self, child: Type[Hy3RecordGroup | Hy3Record]) -> None:
        if not self._child_allowed(child):
            raise Exception("Child record type is not allowed in this parent.")
        self.children.append(child)

    def remove_child(self, child: Type['Hy3Record']) -> None:
        self.children.remove(child)

    def pop_child(self, index: int) -> Type['Hy3Record']:
        return self.children.pop(index)

    def print_tree(self, depth: int = 0) -> None:
        print("  " * depth + str(self))
        for child in self.children:
            child.print_tree(depth + 1)

    def _group_allowed(self, record: Type[Hy3Record]) -> bool:
        if record.record_type[0] != self.record_type[0]:
            return False
        if int(record.record_type[1]) <= int(self.record_type[1]):
            return False
        return True

    def add_to_group(self, record: Type[Hy3Record]) -> Hy3RecordGroup:
        if not self._group_allowed(record):
            raise Exception("Cannot group records")
        group = Hy3RecordGroup(self, record)
        return group

    def to_json(self) -> dict:
        data = {}
        for field in self.fields:
            value = self.data.get(field.name)
            if isinstance(value, datetime.time):
                data[field.name] = value.isoformat()
            elif isinstance(value, datetime.date):
                data[field.name] = value.isoformat()
            else:
                data[field.name] = self.data.get(field.name)
        return {
            "type": "record",
            "record_type": self.record_type,
            "data": data,
            "children": [child.to_json() for child in self.children]
        }

    def to_line(self) -> bytes:
        # record type is first, 2 lines
        result = b""
        result += self.record_type.encode("utf-8")
        for field in self.fields:
            # truncate at length
            data = str(self.data["field"])[:field.length]
            if len(data) != len(self.data["field"]):
                print("Truncated data")
            result += data.encode("utf-8")
            if (tw := len(data)) < field.length:
                result += (" " * (field.length - tw)).encode("utf-8")
        # checksum
        # ensure line is 128 wide
        if len(result) > 128:
            raise Exception("Bad line width")
        elif len(result) < 128:
            result += (" " * (128 - len(result))).encode("utf-8")
        result += self.calculate_checksum(result)
        return result

    @classmethod
    def parse_record(cls, line: bytes):
        if cls is Hy3Record:
            return cls(line)
        given_checksum = line[-2:]
        if cls.calculate_checksum(line[:-2]) != given_checksum:
            print(line, type(line))
            raise Exception("Bad checksum")
        params = {}
        index = 2
        for field in cls.fields:
            data = line[index:index + field.length]
            index += field.length
            params[field.name] = field.type(data.decode("utf-8", errors="replace").strip())
        return cls(line, **params)

    @staticmethod
    def calculate_checksum(line: bytes) -> bytes:
        sum_even = sum_odd = 0
        for i, b in enumerate(line):
            if i % 2 == 0:
                sum_even += b
            else:
                sum_odd += 2 * b
        checksum = math.floor((sum_even + sum_odd) / 21) + 205
        ones = int(checksum % 10)
        tens = int(checksum / 10 % 10)
        return f"{ones}{tens}".encode("utf-8")


# file metadata
class Hy3A1Record(Hy3Record):
    record_type = "A1"
    fields = [
        Field(name="file_code", length=2, type=int),
        Field(name="file_description", length=25),
        Field(name="software_vendor", length=15),
        Field(name="software_name", length=14),
        Field(name="creation_date", length=9, type=date),
        Field(name="creation_time", length=8, type=time),
        Field(name="team_name", length=53)
    ]


# meet data
class Hy3B1Record(Hy3Record):
    record_type = "B1"
    fields = [
        Field(name="meet_name", length=45),
        Field(name="meet_facility", length=45),
        Field(name="meet_start", length=8, type=date),
        Field(name="meet_end", length=8, type=date),
        Field(name="entry_due_date", length=8, type=date),
        Field(name="elevation", length=12, type=int)
    ]


class Hy3B2Record(Hy3Record):
    record_type = "B2"
    fields = [
        Field(name="meet_name", length=45),
        Field(name="meet_host", length=45),
        Field(name="unk", length=6),  # Unknown data
        Field(name="course_code", length=2),
        Field(name="entry_fee", length=6, type=float),
        Field(name="sanction_number", length=11),
    ]


# team data
class Hy3C1Record(Hy3Record):
    record_type = "C1"
    fields = [
        Field(name="team_code", length=5),
        Field(name="team_name", length=30),
        Field(name="team_name_short", length=15),
        Field(name="lsc_code", length=3),
        # some more mumbo jumbo at the end, idk what it means
    ]


class Hy3C2Record(Hy3Record):
    record_type = "C2"
    fields = [
        Field(name="address_1", length=30),
        Field(name="address_2", length=30),
        Field(name="city", length=30),
        Field(name="state", length=2),
        Field(name="postal", length=10),
        Field(name="country", length=3),
        # maybe reg code goes here?
    ]


class Hy3C3Record(Hy3Record):
    record_type = "C3"
    fields = []
    # here for completeness, contains contact info


# Swimmer data
class Hy3D1Record(Hy3Record):
    record_type = "D1"
    fields = [
        Field(name="gender", length=1),
        Field(name="db_id", length=5),
        Field(name="last_name", length=20),
        Field(name="first_name", length=20),
        Field(name="preferred_name", length=20),
        Field(name="middle_initial", length=1),
        Field(name="id", length=14),
        Field(name="unk", length=5),  # random 4 nums b4 bday?
        Field(name="date_of_birth", length=8, type=date),
        Field(name="age", length=3, type=int),
        #      0       USA         N
        # idk what that means
    ]


# race data
class Hy3E1Record(Hy3Record):
    record_type = "E1"
    fields = [
        Field(name="swimmer_gender", length=1),
        Field(name="swimmer_db_id", length=5),
        Field(name="swimmer_name_short", length=5),
        Field(name="gender", length=2),  # MM, FW, XX, MB, FG
        Field(name="distance", length=6, type=int),
        Field(name="stroke_id", length=1),
        Field(name="lower_age", length=3, type=int),
        Field(name="upper_age", length=3, type=int),
        Field(name="unk", length=4),
        Field(name="entry_fee", length=6, type=float),
        Field(name="event_number", length=4),
        Field(name="seed_time_1", length=8),
        Field(name="seed_unit_1", length=1),
        Field(name="seed_time_2", length=8),
        Field(name="seed_unit_2", length=1),
        # random data
    ]


class Hy3E2Record(Hy3Record):
    record_type = "E2"
    fields = [
        Field(name="result_type", length=1),
        Field(name="time", length=8),
        Field(name="time_unit", length=1),
        Field(name="time_code", length=7),
        Field(name="unk", length=1),
        Field(name="heat", length=3),
        Field(name="lane", length=3),
        Field(name="heat_place", length=3),
        Field(name="place", length=4),
        Field(name="unk2", length=3),
        Field(name="time_b1", length=8),
        Field(name="time_b2", length=8),
        Field(name="time_b3", length=8),
        Field(name="dq_code", length=5),  # idk what to call this
        Field(name="time_tp", length=8),
        Field(name="time_unk", length=9),
        Field(name="date", length=13, type=date),
    ]


# relays
class Hy3F1Record(Hy3Record):
    record_type = "F1"
    fields = [
        Field(name="team_code", length=5),
        Field(name="relay_team", length=1),
        Field(name="unk", length=4),
        Field(name="gender", length=2),
        Field(name="unk2", length=1),
        Field(name="distance", length=6, type=int),
        Field(name="stroke_id", length=1),
        Field(name="lower_age", length=3, type=int),
        Field(name="upper_age", length=3, type=int),
        Field(name="unk3", length=4),
        Field(name="entry_fee", length=6, type=float),
        Field(name="event_number", length=4),
        Field(name="seed_time_1", length=8),
        Field(name="seed_unit_1", length=1),
        Field(name="seed_time_2", length=8),
        Field(name="seed_unit_2", length=1),
    ]


class Hy3F2Record(Hy3Record):
    record_type = "F2"
    fields = [
        Field(name="result_type", length=1),
        Field(name="time", length=8),
        Field(name="time_unit", length=1),
        Field(name="time_code", length=7),
        Field(name="unk", length=1),
        Field(name="heat", length=3),
        Field(name="lane", length=3),
        Field(name="heat_place", length=3),
        Field(name="place", length=4),
        Field(name="unk2", length=3),
        Field(name="time_b1", length=8),
        Field(name="time_b2", length=8),
        Field(name="time_b3", length=8),
        Field(name="dq_code", length=5),  # idk what to call this
        Field(name="time_tp", length=8),
        Field(name="time_unk", length=9),
        Field(name="date", length=28, type=date),
    ]


class Hy3F3Record(Hy3Record):
    record_type = "F3"
    fields = [
        Field(name="swimmer_1_gender", length=1),
        Field(name="swimmer_1_db_id", length=5),
        Field(name="swimmer_1_name_short", length=5),
        Field(name="swimmer_1_leg", length=2),
        Field(name="swimmer_2_gender", length=1),
        Field(name="swimmer_2_db_id", length=5),
        Field(name="swimmer_2_name_short", length=5),
        Field(name="swimmer_2_leg", length=2),
        Field(name="swimmer_3_gender", length=1),
        Field(name="swimmer_3_db_id", length=5),
        Field(name="swimmer_3_name_short", length=5),
        Field(name="swimmer_3_leg", length=2),
        Field(name="swimmer_4_gender", length=1),
        Field(name="swimmer_4_db_id", length=5),
        Field(name="swimmer_4_name_short", length=5),
        Field(name="swimmer_4_leg", length=2),
    ]


# Split times
class Hy3G1Record(Hy3Record):
    record_type = "G1"
    fields = [
        Field(name="split_1_unk", length=1),
        Field(name="split_1_lengths", length=2),
        Field(name="split_1_time", length=8),
        Field(name="split_2_unk", length=1),
        Field(name="split_2_lengths", length=2),
        Field(name="split_2_time", length=8),
        Field(name="split_3_unk", length=1),
        Field(name="split_3_lengths", length=2),
        Field(name="split_3_time", length=8),
        Field(name="split_4_unk", length=1),
        Field(name="split_4_lengths", length=2),
        Field(name="split_4_time", length=8),
        Field(name="split_5_unk", length=1),
        Field(name="split_5_lengths", length=2),
        Field(name="split_5_time", length=8),
        Field(name="split_6_unk", length=1),
        Field(name="split_6_lengths", length=2),
        Field(name="split_6_time", length=8),
        Field(name="split_7_unk", length=1),
        Field(name="split_7_lengths", length=2),
        Field(name="split_7_time", length=8),
        Field(name="split_8_unk", length=1),
        Field(name="split_8_lengths", length=2),
        Field(name="split_8_time", length=8),
        Field(name="split_9_unk", length=1),
        Field(name="split_9_lengths", length=2),
        Field(name="split_9_time", length=8),
        Field(name="split_10_unk", length=1),
        Field(name="split_10_lengths", length=2),
        Field(name="split_10_time", length=8),
    ]


# DQ codes I think
class Hy3H1Record(Hy3Record):
    record_type = "H1"
    fields = [
        Field(name="code", length=2),
        Field(name="description", length=122),
    ]


class Hy3H2Record(Hy3H1Record):
    record_type = "H2"


RECORD_TYPES: dict[str, Type[Hy3Record]] = {}

for attr in list(globals().values()):
    if attr is Hy3Record:
        continue
    if not isinstance(attr, type):
        continue
    if issubclass(attr, Hy3Record):
        RECORD_TYPES[attr.record_type] = attr
