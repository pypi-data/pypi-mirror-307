"""Test CpraToSpraConverter."""

import unittest

from snvmodels.chromacmapper import chrom_ac_mapper_grch37
from snvmodels.converters.cpratospraconverter import CpraToSpraConverter
from snvmodels.cpra import Cpra


class CpraToSpraConverterTestCase(unittest.TestCase):
    """Test CpraToSpraConverter."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cpra_to_spra_converter = CpraToSpraConverter(
            chrom_ac_mapper=chrom_ac_mapper_grch37
        )
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
