"""
Testing for the construe package.
"""

##########################################################################
## Imports
##########################################################################

import unittest

##########################################################################
## Module Constants
##########################################################################

TEST_VERSION = "0.1"

##########################################################################
## Test Cases
##########################################################################


class InitializationTest(unittest.TestCase):

    def test_initialization(self):
        """
        Tests a simple world fact by asserting that 10*10 is 100.
        """
        self.assertEqual(2**3, 8)

    def test_import(self):
        """
        Can import confire
        """
        try:
            import construe
        except ImportError:
            self.fail("Unable to import the construe module!")

    def test_version(self):
        """
        Assert that the version is sane
        """
        import construe

        self.assertEqual(TEST_VERSION, construe.__version__)
