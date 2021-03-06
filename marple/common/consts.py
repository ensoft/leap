# ---------------------------------------------
# consts.py - Various enums and other constants
# August 2018 - Andrei Diaconu
# ---------------------------------------------

"""
Module that defines various enums and constants used althroughout the interface
and display modules so that we avoid hard coded things and improve readability

"""

__all__ = (
    "DisplayOptions",
    "InterfaceTypes",
)

from enum import Enum


class DisplayOptions(Enum):
    # The values here should correspond to the ones from the config
    HEATMAP = "heatmap"
    STACKPLOT = "stackplot"
    FLAMEGRAPH = "flamegraph"
    TREEMAP = "treemap"
    G2 = "g2"
    TCPPLOT = "plot"


class InterfaceTypes(Enum):
    # The values here should correspond to the ones from the config
    SCHEDEVENTS = 'cpusched'
    DISKLATENCY = 'disklat'
    MALLOCSTACKS = 'mallocstacks'
    MEMLEAK = 'memusage'
    MEMTIME = 'memtime'
    CALLSTACK = 'callstack'
    TCPTRACE = 'ipc'
    MEMEVENTS = 'memevents'
    DISKBLOCK = 'diskblockrq'
    PERF_MALLOC = 'perf_malloc'


class Datatypes(Enum):
    STACK = 'stack'
    EVENT = 'event'
    POINT = 'point'


# Display modes for the interfaces
display_dictionary = {
    Datatypes.EVENT: [DisplayOptions.G2, DisplayOptions.TCPPLOT],
    Datatypes.STACK: [DisplayOptions.TREEMAP,
                      DisplayOptions.FLAMEGRAPH],
    Datatypes.POINT: [DisplayOptions.HEATMAP, DisplayOptions.STACKPLOT],
}

# All the interfaces detected by the collect module
interfaces_argnames = [interface.value for interface in InterfaceTypes]

# Separator used by the datatypes to separate their fields
field_separator = "$$$"

# Separator used to separate sections in the .marple files
section_separator = "\n"
