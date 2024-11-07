"""Test CpraToCspraConverter."""

import unittest

from snvmodels.chromacmapper import chrom_ac_mapper_grch37
from snvmodels.converters.cpratocspraconverter import CpraToCspraConverter
from snvmodels.cpra import Cpra


class CpraToCspraConverterTestCase(unittest.TestCase):
    """Test CpraToCspraConverter."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cpra_to_cspra_converter = CpraToCspraConverter(
            chrom_ac_mapper=chrom_ac_mapper_grch37
        )
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
