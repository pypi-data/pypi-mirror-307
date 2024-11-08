"""Test Cpra class."""

import unittest

from snvmodels.cpra import Cpra


class CpraTestCase(unittest.TestCase):
    """Test Cpra class."""

    def test_init(self):
        """Test initialization of Cpra instance."""
        cpra = Cpra(chrom="chr1", pos=1, ref="A", alt="T")
        self.assertTrue(isinstance(cpra, Cpra))
