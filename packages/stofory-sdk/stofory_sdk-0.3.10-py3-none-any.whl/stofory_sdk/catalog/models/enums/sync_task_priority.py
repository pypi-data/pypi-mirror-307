import enum


class SyncTaskPriority(enum.StrEnum):
    CRITICAL = enum.auto()
    REGULAR = enum.auto()
    BACKGROUND = enum.auto()
