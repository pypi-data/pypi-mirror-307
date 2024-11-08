"""Test ChromAcMapper of GRCh37 p13."""

import unittest

from snvmodels.chromacmapper import chrom_ac_mapper_grch37


class ChromAcMapperGrch37p13TestCase(unittest.TestCase):
    """Test ChromAcMapper of GRCh37 p13."""

    def test_ac_to_chrom(self):
        self.assertEqual(chrom_ac_mapper_grch37.ac_to_chrom(ac="NC_000001.10"), "chr1")

    def test_chrom_to_ac(self):
        self.assertEqual(
            chrom_ac_mapper_grch37.chrom_to_ac(chrom="chrX"), "NC_000023.10"
        )
