# -------------------------------------------------------------
# flamegraph.py - interacts with the flame graph tool
# June-July 2018 - Franz Nowak, Hrutvik Kanabar
# -------------------------------------------------------------
"""
Interacts with the flamegraph tool.

Issues a command to start the necessary scripts in Brendan Gregg's
Flamegraph tool.

"""
import os
import subprocess

DISPLAY_DIR = str(os.path.dirname(os.path.dirname(os.path.realpath(
              __file__)))) + "/"

FLAMEGRAPH_DIR = DISPLAY_DIR + "util/flamegraph/flamegraph.pl"


def make(in_filename, out_filename, colouring=None):
    """
    Uses Brendan Gregg's flamegraph tool to convert data to flamegraph.

    :param in_filename:
        The name of the data file from which to create the image.
    :param out_filename:
        The name of the image file that will be created.

    """
    with open(out_filename, "w") as out:
        if colouring:
            subprocess.Popen([FLAMEGRAPH_DIR, "--color=" + colouring,in_filename], stdout=out)
        else:
            subprocess.Popen([FLAMEGRAPH_DIR, in_filename], stdout=out)

def show(image):
    """
    Uses firefox to display the flamegraph.

    :param image:
        The image file containing the flamegraph.

    """
    username = os.environ['HOME'][6:]  # @@@ TODO find a better way of doing this
    subprocess.call(["su", "-", "-c",  "firefox " + DISPLAY_DIR + image,
                     username])

