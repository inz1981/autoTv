#!/usr/bin/env python
import sys
import os
import unittest
import logging
sys.path.append(os.path.join(os.path.dirname(__file__), '../src/'))


class TestTVParser(unittest.TestCase):
    def setUp(self):
        self.log = logging.getLogger(__name__)

    def test_read_dl_dir(self):
        """
        Test that download dir can be read
        """
        from config.config import Config
        from filehandle.io import TVParser
        cfg = Config(os.path.join(os.path.dirname(__file__),
                                  'config/tests.cfg'))
        tvp = TVParser(cfg)
        self.log.info(tvp.dl_content)
        self.assertEqual(len(tvp.dl_content), 4)
