#!/usr/bin/env python
"""
Main script for autotv
"""
from __future__ import absolute_import, division, print_function,\
    unicode_literals
import logging
import optparse

from config import Config
from common import utils
from filehandle import TVParser, MovieParser


def main():
    """
    Main function
    """
    log = logging.getLogger(__name__)
    log.info("Starting AutoTV")

    usage = "%prog -c FILE [--debug]"

    # the version of Auto TV.
    version = "0.1"

    parser = optparse.OptionParser(usage=usage, version=version)
    parser.add_option(
        "-c", "--config",
        dest="config_file",
        help="the config file(e.g. autotv.cfg)",
        metavar="FILE")

    parser.add_option(
        "--debug",
        action="store_true",
        dest="verbose",
        default=False,
        help="print more info")

    options, _ = parser.parse_args()

    # setup logging
    if options.verbose:
        # set logging to debug
        utils.setup_logging(logging.DEBUG)
    else:
        utils.setup_logging(logging.INFO)

    log.debug("Input arguments: {%s}".format(options))

    # the config file is mandatory
    if not options.config_file:
        parser.error("Missing mandatory argument: '-c/--config'")

    log.info('Starting Auto TV...')

    # read the config
    cfg = Config(options.config_file)
    # cfg_options = cfg.cfg_options

    # Start TV Parsing
    tvp = TVParser(cfg)
    if options.verbose:
        tvp.store_debug_info()
    copy_tvs = tvp.get_unstored_tv_contents()
    tvp.transfer_tv_contents(copy_tvs)

    # Start Movie Parsing
    movieparser = MovieParser(cfg)
    if options.verbose:
        movieparser.store_debug_info()

    log.info("exit!")

if __name__ == '__main__':
    main()
