"""Test CpraToCspraGrch37Converter."""

import unittest

from snvmodels.converters.cpratocspragrch37converter import CpraToCspraGrch37Converter
from snvmodels.cpra import Cpra


class CpraToCspraGrch37ConverterTestCase(unittest.TestCase):
    """Test CpraToCspraGrch37Converter."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cpra_to_cspra_converter = CpraToCspraGrch37Converter()
        cpra = Cpra(chrom="chr1", pos=1, ref="A", alt="T")
        cls.cspra = cpra_to_cspra_converter.convert(cpra=cpra)

    def test_chrom(self):
        self.assertEqual(self.cspra.chrom, "chr1")

    def test_ac(self):
        self.assertEqual(self.cspra.ac, "NC_000001.10")

    def test_pos(self):
        self.assertEqual(self.cspra.pos, 1)

    def test_ref(self):
        self.assertEqual(self.cspra.ref, "A")

    def test_alt(self):
        self.assertEqual(self.cspra.alt, "T")
