# -------------------------------------------------------------
# data_types.py - intermediate form of data to be converted
# June-July 2018 - Franz Nowak
# -------------------------------------------------------------

"""Data types for intermediate formats used in later data processing."""

from typing import NamedTuple


class SchedEvent(NamedTuple):
    """Represents a single scheduler event."""
    name: str
    pid: int
    cpu: str
    time: str
    type: str
