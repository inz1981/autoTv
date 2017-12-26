#!/usr/bin/env python
from __future__ import absolute_import, division, print_function,\
    unicode_literals

import logging
import optparse
import os
import pprint

from config.config import Config

from src.common import utils
from src.filehandle import TVParser


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
        utils.setup_logging(logging.DEBUG)
    else:
        utils.setup_logging(logging.INFO)

    log.debug("Input arguments: {0}".format(options))

    # the config file is mandatory
    if not options.config_file:
        parser.error("Missing mandatory argument: '-c/--config'")

    log.info('Starting Auto TV...')

    # read the config
    cfg = Config(options.config_file)
    cfg_options = cfg.cfg_options
    # Unrar all the content in download dir
    # rar_archive = RarArchive()
    # rar_archive.unrar_folders_recursive(
    #     cfg_options['storage']['download_folder'],
    #     cfg_options['general']['delete_archive'])

    # Start TV Parsing
    tvp = TVParser(cfg_options)

    utils.save_json(tvp.dl_content, 'content_dl.json')
    utils.save_json(tvp.tv_contents, 'content_tv.json')
    utils.save_json(tvp.tv_contents_matched, 'content_tv_matched.json')

    tvp.get_unstored_tv_contents()
    exit()
    log.debug("Found matched TV series\n{0}".format(pprint.pformat(matched_tv)))
    log.info("-- Begin iterations")
    for content in content_dl:
        # tvp.detect_tv_show(file)
        log.info("content: {}".format(content))
        # check if tv show already exist
        if 'tv' in content and content['tv'] in matched_tv:
            log.warning(
                "The following TV Show is already stored in ({1})\n({0})"
                .format(content['tv'],
                        cfg_options['storage']['tv_folder'])
            )
            continue
        elif 'type' in content and content['type'] == 'RAR':
            # unrar the TV show to TV dir
            tvp.unrar_archive(
                content['filepath'], dest=os.path.join(
                     cfg_options['storage']['tv_folder'],
                     content['tv']['show_dot'])
            )

    # Copy files to TV Folder in case no RAR archive.
    # for content in content_dl:
    #     if 'tv' in content:
    #         log.info("Copy files from \n{0}".format(pprint.pformat(content)))
    # log.info(pprint.pformat(matched_tv))
    print("exit!")

if __name__ == '__main__':
    main()
