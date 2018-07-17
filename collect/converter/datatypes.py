# -------------------------------------------------------------
# datatypes.py - intermediate form of data to be converted
# June-July 2018 - Franz Nowak
# -------------------------------------------------------------

"""Data types for intermediate formats used in later data processing."""

from typing import NamedTuple


class SchedEvent(NamedTuple):
    """Represents a single scheduler event."""
    name: str
    pid: int
    cpu: int
    time: str
    type: str


class StackEvent(NamedTuple):
    """Represents a single call stack"""
    # Could have more attributes if needed
    stack: tuple