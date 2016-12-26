def parse_config(config_file):
    """
    Factory function to parse the config_file, determine the parameters
    locate the class handling the respective actions or create a new sub-class
    of Config dynamically if the

    :param config_file: the autotv config file (ini format)
    :return: obj, a autotv.Config subclass
    """
    import ConfigParser
    import logging
    import json
    import os
    import sys
    log = logging.getLogger('parse_config')
    log.info('Starting to parse config file ({0})'.format(config_file))

    defaults = {}
    cfg = ConfigParser.SafeConfigParser(defaults=defaults)
    if not os.path.exists(config_file):
        log.error("Could not find file ({0})".format(config_file))
        sys.exit(0)

    cfg.read(config_file)

    sections = ['storage']

    for sec in sections:
        log.debug('Fetching section ({0}) parameters'.format(sec))
        try:
            dl_dir = cfg.get(sec, 'download_dir').strip()
        except (ConfigParser.NoOptionError,
                ConfigParser.NoSectionError) as exp:
            log.warn(exp)
            continue
        log.debug('Got ({0}) parameter'.format(dl_dir))
