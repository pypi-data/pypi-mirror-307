"""Test CpraHgvsChrFormatter class."""

import unittest

from snvmodels.cpra import Cpra
from snvmodels.cpra.formatters import CpraHgvsChrFormatter


class CpraHgvsChrFormatterTestCase(unittest.TestCase):
    """Test CpraHgvsChrFormatter class."""

    def test_format_case1(self):
        """Test initialization of Cpra instance case 1."""
        cpra = Cpra(chrom="chr1", pos=1, ref="A", alt="T")
        hgvs_chr = CpraHgvsChrFormatter().format(cpra=cpra)
        self.assertEqual(hgvs_chr, "chr1:g.1A>T")

    def test_format_case2(self):
        """Test initialization of Cpra instance case 2."""
        cpra = Cpra(chrom="2", pos=17142, ref="G", alt="GA")
        hgvs_chr = CpraHgvsChrFormatter().format(cpra=cpra)
        self.assertEqual(hgvs_chr, "chr2:g.17142_17143insA")

    def test_format_case3(self):
        """Test initialization of Cpra instance case 3."""
        cpra = Cpra(chrom="MT", pos=8270, ref="CACCCCCTCT", alt="C")
        hgvs_chr = CpraHgvsChrFormatter().format(cpra=cpra)
        self.assertEqual(hgvs_chr, "chrMT:g.8271_8279del")

    def test_format_case4(self):
        """Test initialization of Cpra instance case 4."""
        cpra = Cpra(chrom="X", pos=107930849, ref="GGA", alt="C")
        hgvs_chr = CpraHgvsChrFormatter().format(cpra=cpra)
        self.assertEqual(hgvs_chr, "chrX:g.107930849_107930851delinsC")
