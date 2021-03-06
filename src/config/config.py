import logging
import os
import pprint
import sys
if sys.version_info < (3, 0):
    import ConfigParser as cp
else:
    import configparser as cp


class Config:
    """
    Config class for handling config files (ini)
    """
    def __init__(self, config_path):
        """
        Loding the config file, storing each section in dict
        :param config_path: the path to the config file
        """
        self.log = logging.getLogger(__name__)
        self.cfg_file = os.path.abspath(config_path)
        self.cfg = None
        self.read_cfg()
        # dict data of config
        self.cfg_contents = None
        self.cfg_sections = ['general', 'storage']

    def read_cfg(self):
        """
        Read input config file and setup ConfigParser
        """
        if not os.path.isfile(self.cfg_file):
            raise IOError('No such file ({0})'.format(self.cfg_file))
        self.log.info("Reading config file from ({0})".format(self.cfg_file))
        self.cfg = cp.ConfigParser()
        self.cfg.read(self.cfg_file)

    def config_section_map(self, section):
        """
        Parsing a section of INI config
        :param section: str, the name of the section
        :return: dict, with the parameters-values
        {
            'download_folder': '/media/downloads/',
            'movie_folder': '/media/movies/',
            'torrent_folder': '/media/torrents/',
            'tv_folder': '/media/tv/'
        }
        """
        result = {}
        options = self.cfg.options(section)
        for option in options:
            try:
                result[option] = self.cfg.get(section, option)
                if result[option] == -1:
                    self.log.warning("skip: %s" % option)
            except:
                self.log.warning("exception on %s!" % option)
                result[option] = None
        return result

    @property
    def cfg_options(self):
        """
        Parses the config ini file and stores each section and parameters-
        values in a dict
        :return: dict, of format below:
        {
        'general':
            {
                'delete_archive': 'true',
                'unrar_path': '/usr/bin/unrar'
            },
        'storage':
            {
                'download_folder': '/media/downloads/',
                'movie_folder': '/media/movies/',
                'torrent_folder': '/media/torrents/',
                'tv_folder': '/media/tv/'
            }
        }
        """
        if self.cfg_contents is not None:
            return self.cfg_contents

        self.cfg_contents = {}
        for section in self.cfg_sections:
            self.log.debug("parsing section: {0}".format(section))
            self.cfg_contents[section] = self.config_section_map(section)
        self.log.debug("cfg_options:\n{0}".format(pprint.pformat(
            self.cfg_contents)))
        return self.cfg_contents

    def get_debug_storage(self):
        """
        Get the debug folder to store files in
        :return: path to debug folder or None
        """
        if 'debug_folder' in self.cfg_contents['storage']:
            return self.cfg_contents['storage']['debug_folder']
        return None
