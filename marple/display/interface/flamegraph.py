# -------------------------------------------------------------
# flamegraph.py - interacts with the flame graph tool
# June-July 2018 - Franz Nowak, Hrutvik Kanabar
# -------------------------------------------------------------
"""
Class that interacts with the flamegraph tool.

Implements the GenericDiaplay interface to display an interactive flamegraph
in the browser.

"""

__all__ = (
    "Flamegraph",
)

import collections
import logging
import os
import subprocess
from typing import NamedTuple

from marple.common import (
    config,
    consts,
    file,
    util,
    paths
)
from marple.display.interface.generic_display import GenericDisplay

logger = logging.getLogger(__name__)
logger.debug('Entered module: %s', __name__)

FLAMEGRAPH_DIR = paths.MARPLE_DIR + "/display/tools/flamegraph/flamegraph.pl"


class Flamegraph(GenericDisplay):
    """
    The class representing flamegraphs.

    """
    class DisplayOptions(NamedTuple):
        """
        - coloring: can be hot (default), mem, io, wakeup, chain, java, js,
                    perl, red, green, blue, aqua, yellow, purple, orange
        """
        coloring: str

    def __init__(self, data):
        """
        Initialise the flamegraph.

        :param data:
            A `data_io.StackData` object that encapsulated the collected data
            we want to display as a flamegraph

        """
        # Initialise the base class
        super().__init__(data)

        coloring = config.get_option_from_section(
            consts.DisplayOptions.FLAMEGRAPH.value, "coloring")
        self.display_options = self.DisplayOptions(coloring)
        self.svg_temp_file = str(file.TempFileName())

    @util.log(logger)
    def _make(self):
        """
        Uses Brendan Gregg's flamegraph tool to convert data to flamegraph.

        """
        stacks_temp_file = str(file.TempFileName())
        counts = collections.Counter()

        stack_data = self.data.datum_generator
        for stack in stack_data:
            new_counts = collections.Counter({stack.stack: stack.weight})
            counts += new_counts

        with open(stacks_temp_file, "w") as out:
            for stack, count in counts.items():
                out.write(";".join(stack) + " {}\n".format(count))

        with open(self.svg_temp_file, "w") as out:
            if self.display_options.coloring:
                sp = subprocess.Popen(
                        [FLAMEGRAPH_DIR, "--color=" +
                         self.display_options.coloring,
                         "--countname=" + self.data_options.weight_units,
                         stacks_temp_file], stdout=out)
            else:
                sp = subprocess.Popen([FLAMEGRAPH_DIR, stacks_temp_file],
                                      stdout=out)
        # Wait for the subprocess to generate the svg file so the show method
        # doesn't try to open it while it's being written to
        sp.wait()

        return counts  # for testing

    @util.log(logger)
    @util.Override(GenericDisplay)
    def show(self):
        """
        Creates the image and uses firefox to display the flamegraph.

        """
        # Create a flamegraph svg based on the data
        self._make()

        # Open firefox
        username = os.environ['SUDO_USER']
        subprocess.call(
            ["su", "-", "-c",  "firefox " + self.svg_temp_file, username])
