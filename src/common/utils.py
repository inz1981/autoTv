import logging

def setup_logging(level):
    """
    Setting up the logging level for logger
    :param level: level, debug/info
    """
    log_fmt = '%(asctime)s - %(name)s - %(levelname)-8s > %(message)s'
    logger = logging.getLogger()
    logger.setLevel(level)
    formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def save_json(content, filename):
    import json
    logger = logging.getLogger(__name__)
    with open(filename, 'w') as outfile:
        json.dump(content, outfile, indent=4)
    logger.info("written file: {0}".format(filename))
