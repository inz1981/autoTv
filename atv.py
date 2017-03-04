#!/usr/bin/env python
import optparse
import logging
import sys
from common import logger
from filehandle import TVParser
from config import Config


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
        help="the config file(e.g. autotv.cfg)",
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

    cfg = Config(options.config_file)
    cfg_options = cfg.cfg_options

    # read the config
    # config = parse_config(options.config_file)

    # TODO: The rest of the program...


    # io = IOParser(config['dl_dir'])
    # files = io.read_path('rar')

    tvp = TVParser(cfg_options['storage']['download_folder'])
    dl_content = tvp.scan_download_dir(
        cfg_options['storage']['download_folder'])
    dl_content = tvp.scan_download_dir(
        cfg_options['storage']['download_folder'])
    sys.exit()
    tvp.get_media_type()
    # files = tvp.read_path('rar')
    # for file in files:
    # tvp.detect_tv_show(file)
    # if file.endswith('.rar'):
    # tvp.unrar_archive(file)
    print "exit!"

if __name__ == '__main__':
    main()
