def setup_logging(level):
    """
    Setting up the logging level for logger
    :param level: level, debug/info
    """
    import logging
    log_fmt = '%(asctime)s - %(levelname)-8s > %(message)s'
    logger = logging.getLogger()
    logger.setLevel(level)
    formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
