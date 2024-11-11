"""Test CpraOncokbGenomicChangeFormatter class."""

import unittest

from snvmodels.cpra import Cpra
from snvmodels.cpra.formatters import CpraOncokbGenomicChangeFormatter


class CpraOncokbGenomicChangeFormatterTestCase(unittest.TestCase):
    """Test CpraOncokbGenomicChangeFormatter class."""

    def test_format_case1(self):
        """Test initialization of Cpra instance case 1."""
        cpra = Cpra(chrom="chr1", pos=1, ref="A", alt="T")
        hgvs_chr = CpraOncokbGenomicChangeFormatter().format(cpra=cpra)
        self.assertEqual(hgvs_chr, "1,1,1,A,T")

    def test_format_case2(self):
        """Test initialization of Cpra instance case 2."""
        cpra = Cpra(chrom="2", pos=17142, ref="G", alt="GA")
        hgvs_chr = CpraOncokbGenomicChangeFormatter().format(cpra=cpra)
        self.assertEqual(hgvs_chr, "2,17142,17142,G,GA")

    def test_format_case3(self):
        """Test initialization of Cpra instance case 3."""
        cpra = Cpra(chrom="MT", pos=8270, ref="CACCCCCTCT", alt="C")
        hgvs_chr = CpraOncokbGenomicChangeFormatter().format(cpra=cpra)
        self.assertEqual(hgvs_chr, "MT,8270,8279,CACCCCCTCT,C")

    def test_format_case4(self):
        """Test initialization of Cpra instance case 4."""
        cpra = Cpra(chrom="X", pos=107930849, ref="GGA", alt="C")
        hgvs_chr = CpraOncokbGenomicChangeFormatter().format(cpra=cpra)
        self.assertEqual(hgvs_chr, "X,107930849,107930851,GGA,C")
