#!/usr/bin/env python

import logging
from common import parse_config, logger
import optparse


def main():
    """Main function
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
        help="the vEPC config file(e.g. vepc.cfg)",
        metavar="FILE")

    parser.add_option(
        "--debug",
        action="store_true",
        dest="verbose",
        default=False,
        help="print more info")

    options, args = parser.parse_args()

    # setup logging
    if options.verbose:
        # set logging to debug
        logger.setup_logging(logging.DEBUG)
    else:
        logger.setup_logging(logging.INFO)

    log.debug("Input arguments: {0}".format(options))

    # the config file is mandatory
    if not options.config_file:
        parser.error("Missing mandatory argument: '-c/--config'")

    log.info('Starting Auto TV...')

    # read the config
    config = parse_config(options.config_file)

    # TODO: The rest of the program...

if __name__ == '__main__':
    main()
