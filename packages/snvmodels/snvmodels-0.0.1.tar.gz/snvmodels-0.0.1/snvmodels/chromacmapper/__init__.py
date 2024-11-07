"""Chromosome-sequence-accession mapper."""

from .chromacmapper import ChromAcMapper
from .creators import NcbiChromAcMapperCreator

url_grch37_p13 = "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.25_GRCh37.p13/GCF_000001405.25_GRCh37.p13_assembly_report.txt"
chrom_ac_mapper_grch37 = NcbiChromAcMapperCreator(url=url_grch37_p13).create()
