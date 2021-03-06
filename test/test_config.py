#!/usr/bin/env python
import sys
import os
import logging
import unittest


class TestConfig(unittest.TestCase):
    def setUp(self):
        sys.path.append(os.path.join(os.path.dirname(__file__), '../src/'))
        self.logger = logging.getLogger(__name__)

    def test_load_config(self):
        """
        Test that config class can be instantiated
        """
        from config import Config

        cfg = Config(os.path.join(os.path.dirname(__file__),
                                  'config/tests.cfg'))
        self.assertTrue(isinstance(cfg, Config))
