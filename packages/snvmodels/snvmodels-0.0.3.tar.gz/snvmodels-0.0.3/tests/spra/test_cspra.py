"""Test Cspra class."""

import unittest

from snvmodels.spra import Cspra


class CspraTestCase(unittest.TestCase):
    """Test Cspra class."""

    def test_init(self):
        """Test initialization of Cspra instance."""
        cspra = Cspra(chrom="chr1", ac="NC_000001.10", pos=1, ref="A", alt="T")
        self.assertTrue(isinstance(cspra, Cspra))
