#!/usr/bin/env python
import sys
import os
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '../src/'))


class TestConfig(unittest.TestCase):

    def test_load_config(self):
        """
        Test that config class can be instantiated
        """
        from config.config import Config

        cfg = Config(os.path.join(os.path.dirname(__file__),
                                  'config/tests.cfg'))
        self.assertTrue(isinstance(cfg, Config))
