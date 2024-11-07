"""Test Spra class."""

import unittest

from snvmodels.spra import Spra


class SpraTestCase(unittest.TestCase):
    """Test Spra class."""

    def test_init(self):
        """Test initialization of Spra instance."""
        spra = Spra(ac="NC_000001.10", pos=1, ref="A", alt="T")
        self.assertTrue(isinstance(spra, Spra))
