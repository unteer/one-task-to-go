import typing
from dataclasses import dataclass
import datetime
import uuid
from enum import Enum


class TodoStatus:
    inactive = ("deleted", "completed")
    active = ("current", "paused")
    allowed = inactive + active


def _generate_statuses_lookup() -> dict:
    lookup = {}
    lookup["inactive"] = TodoStatus.inactive
    lookup["active"] = TodoStatus.active
    for status in TodoStatus.allowed:
        lookup[status] = (status, )

    return lookup


todostatus_lookup = _generate_statuses_lookup()


@dataclass()
class Preference():
    name: str
    value: str
    updated_on: datetime.datetime


@dataclass
class Todo():
    uuid: uuid.UUID
    description: str
    current_status: str
    created_on: datetime.datetime
    completed_on: datetime.datetime