"""Test NcbiChromAcMapperCreator class."""

import unittest

from snvmodels.chromacmapper.creators import NcbiChromAcMapperCreator


class NcbiChromAcMapperCreatorGrch37p13TestCase(unittest.TestCase):
    """Test NcbiChromAcMapperCreator class with GRCh37 p13."""

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        url = "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.25_GRCh37.p13/GCF_000001405.25_GRCh37.p13_assembly_report.txt"
        creator = NcbiChromAcMapperCreator(url=url)
        cls.creator = creator

    def test_create(self):
        """Test convert method."""
        chrom_ac_mapper = self.creator.create()
        self.assertEqual(chrom_ac_mapper.ac_to_chrom(ac="NC_000001.10"), "chr1")
        self.assertEqual(chrom_ac_mapper.chrom_to_ac(chrom="chrX"), "NC_000023.10")
