# -------------------------------------------------------------
# main.py - user interface, parses and applies commands
# June-July 2018 - Franz Nowak
# -------------------------------------------------------------

"""
Controller script - user interface, parses and applies commands

Handles interaction between the user and the middle level
functionality (mem, sched etc).
It calls the relevant functions for each command.

"""

import argparse
import logging
import os

from . import sched
import src.common.output as output
import src.common.config as config
import src.common.file as file

COLLECTION_TIME = 10

logger = logging.getLogger('controller.main')
logger.setLevel(logging.DEBUG)

__all__ = "main"


def _collect(args):
    """
    Collection part of the controller module.

    Deals with data collection.

    :param args:
        Command line arguments for data-collection.
        Passed by main function.

    """
    logger.info("Collect function. "
                "Applying logic evaluating and applying input parameters")

    # Use the user specified filename if there is one,
    # otherwise create a unique one
    if args.file is None:
        filename = file.create_name()
        logger.info("Trying to generate default filename "
                    "as no filename was specified")
        i = 5
        while os.path.isfile(filename) and i > 0:
            filename = file.create_name()
            i -= 1

        if os.path.isfile(filename):
            output.error_("Unable to create a unique filename. "
                          "Please choose a filename and try again.",
                          "Failed to generate unique filename! Exiting! "
                          "Name: {}".format(filename))
            exit(1)
    else:
        filename = args.file

    if os.path.isfile(filename):
        logger.debug("File already exist. Filename: {}. Throwing exception"
                     .format(filename))
        raise FileExistsError

    # Collect data for user specified amount of time, otherwise standard value
    if args.time is None:
        time = config.get_default_time()
        if time is None:
            time = COLLECTION_TIME
        logger.info("Using default time {}s "
                    "as no time was specified".format(time))
    else:
        time = args.time

    if args.sched:
        logger.info("Recording scheduling data for {} seconds".format(time))
        sched.collect_all(time, filename)

    if args.lib:
        # Stub
        logger.info("Recording library loading data "
                    "for {} seconds".format(time))
    if args.ipc:
        # Stub
        logger.info("Recording ipc data for {} seconds".format(time))
    if args.mem:
        # Stub
        logger.info("Recording memory data for {} seconds".format(time))


def _display(args):
    """
    Displaying part of the controller module.

    Deals with displaying data.

    :param args:
        Command line arguments for data-display
        Passed by main function

    """
    logger.info("Display function."
                "Applying logic evaluating and applying input parameters")

    # Try to use the specified name, otherwise throw exception
    filename = args.file
    if filename is None or not os.path.isfile(filename):
        logger.debug("File not found, throwing exception")
        raise FileNotFoundError

    if args.sched:
        # Stub
        logger.info("Displaying scheduling data")
    elif args.lib:
        # Stub
        logger.info("Displaying library loading data")
    elif args.ipc:
        # Stub
        logger.info("Displaying ipc scheduling data")
    elif args.mem:
        # Stub
        logger.info("Displaying mem scheduling data")


def _args_parse(argv):
    """
    Parse the command line arguments.

    :param argv:
        the arguments passed by the main function

    :return:
        an object containing the parsed command information

    Called by main when the program is started.

    Calls functions _parse_collect and _parse_display to create subparsers
    for collection and display respectively.

    """

    logger.info("Enter _args_parse function. Creates parser parses input")

    # Create parser object
    parser = argparse.ArgumentParser(prog="leap",
                                     description="Collect and display "
                                                 "performance data")

    # Create two sub-parsers for the two kinds of command, collect and display
    subparsers = parser.add_subparsers(dest="command")
    
    _parse_collect(subparsers)

    _parse_display(subparsers)

    logger.info("Parsing input arguments")

    return parser.parse_args(argv)


def _parse_collect(subparsers):
    """
    Parses a collect command.

    Arguments that are created:

        sched: CPU scheduling data
        lib: library load times
        ipc: ipc efficiency
        mem: memory allocation/deallocation

        time t: time in seconds to record data

    :param subparsers:
        subparsers of the main parser, passed by _args_parse

    """

    logger.info("Enter parse_collect function")

    parser_collect = subparsers.add_parser("collect",
                                           help="Collect data to display")

    # Add options for the modules
    module_collect = parser_collect.add_mutually_exclusive_group(required=True)
    module_collect.add_argument("-s", "--sched", action="store_true",
                                help="scheduler module")
    module_collect.add_argument("-l", "--lib", action="store_true",
                                help="library module")
    module_collect.add_argument("-i", "--ipc", action="store_true",
                                help="ipc module")
    module_collect.add_argument("-m", "--mem", action="store_true",
                                help="memory module")

    # Add flag and parameter for filename
    filename = parser_collect.add_argument_group()
    filename.add_argument("-f", "--file", type=str,
                          help="Output file where collected data is stored")

    # Add flag and parameter for time
    time = parser_collect.add_argument_group()
    time.add_argument("-t", "--time", type=int,
                      help="time in seconds that data is collected")

    # Set default function
    parser_collect.set_defaults(func=_collect)


def _parse_display(subparsers):
    """
    Parses a display command.

     Arguments that are created:

        sched: CPU scheduling data
        lib: library load times
        ipc: ipc efficiency
        mem: memory allocation/deallocation

        -n: numerical representation of data
        -g: graphical representation of data

    :param subparsers:
         subparsers of the main parser, passed by _args_parse

    """
    logging.info("enter parse_display function")

    parser_display = subparsers.add_parser("display",
                                           help="Display collected data "
                                                "in required format")

    # Add options for the modules
    module_display = parser_display.add_mutually_exclusive_group(required=True)
    module_display.add_argument("-s", "--sched", action="store_true",
                                help="scheduler module")
    module_display.add_argument("-l", "--lib", action="store_true",
                                help="library module")
    module_display.add_argument("-i", "--ipc", action="store_true",
                                help="ipc module")
    module_display.add_argument("-m", "--mem", action="store_true",
                                help="memory module")

    # Add flag and parameter for displaying type in case of display
    type_display = parser_display.add_mutually_exclusive_group(required=True)
    type_display.add_argument("-n", action="store_true",
                              help="numerical representation as a table")
    type_display.add_argument("-g", action="store_true",
                              help="graphical representation as an image")

    # Add flag and parameter for filename
    filename = parser_display.add_argument_group()
    filename.add_argument("-f", "--file", type=str,
                          help="Input file where collected data "
                               "to display is stored")
    # Set default function
    parser_display.set_defaults(func=_display)


def main(argv):
    """
    The main function of the controller.

    Calls the middle level modules according to options selected by user.

    :param argv:
        command line arguments from call in main

    """
    logger.info("Enter controller main function")

    # Parse arguments
    logger.info("Trying to parse input: {}".format(argv))
    args = _args_parse(argv)

    # Call the appropriate function, either collect or display
    try:
        args.func(args)
    except FileExistsError:
        output.error_("A file with that name already exists. "
                      "Please choose a unique filename.",
                      "filename already exists")
        exit(1)
    except FileNotFoundError:
        output.error_("Error: No file with that name found. "
                      "Please choose a different filename or collect new data.",
                      "file not found")
        exit(1)