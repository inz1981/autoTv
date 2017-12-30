def parse_config(config_file):
    """
    Factory function to parse the config_file, determine the parameters
    locate the class handling the respective actions or create a new sub-class
    of Config dynamically if the

    :param config_file: the autotv config file (ini format)
    :return: obj, a autotv.Config subclass
    """
    import sys
    if sys.version_info < (3, 0):
        import ConfigParser as cp
    else:
        import configparser as cp
    import logging
    import os
    import sys
    cfg_file = os.path.abspath(config_file)
    log = logging.getLogger(__name__)
    log.info('Starting to parse config file ({0})'.format(cfg_file))
    result = {}

    defaults = {}
    cfg = cp.SafeConfigParser(defaults=defaults)
    if not os.path.exists(cfg_file):
        log.error("Could not find file ({0})".format(cfg_file))
        sys.exit(0)

    cfg.read(cfg_file)

    sections = ['storage']

    for sec in sections:
        log.debug('Fetching section ({0}) parameters'.format(sec))
        try:
            dl_dir = os.path.abspath(cfg.get(sec, 'download_dir').strip())
            result['dl_dir'] = dl_dir
            tv_dir = os.path.abspath(cfg.get(sec, 'tv_dir').strip())
            result['tv_dir'] = tv_dir
        except (cp.NoOptionError,
                cp.NoSectionError) as exp:
            log.warn(exp)
            continue
        log.debug('Got ({0}) parameter'.format(dl_dir))
    return result
