"""Test CpraToSpraGrch37Converter."""

import unittest

from snvmodels.converters.cpratospragrch37converter import CpraToSpraGrch37Converter
from snvmodels.cpra import Cpra


class CpraToSpraGrch37ConverterTestCase(unittest.TestCase):
    """Test CpraToSpraGrch37Converter."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cpra_to_spra_converter = CpraToSpraGrch37Converter()
        cpra = Cpra(chrom="chr1", pos=1, ref="A", alt="T")
        cls.spra = cpra_to_spra_converter.convert(cpra=cpra)

    def test_ac(self):
        self.assertEqual(self.spra.ac, "NC_000001.10")

    def test_pos(self):
        self.assertEqual(self.spra.pos, 1)

    def test_ref(self):
        self.assertEqual(self.spra.ref, "A")

    def test_alt(self):
        self.assertEqual(self.spra.alt, "T")
