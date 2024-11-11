"""Convert Cpra to Spra for GRCh37."""

from snvmodels.chromacmapper import chrom_ac_mapper_grch37
from snvmodels.cpra import Cpra
from snvmodels.spra import Spra


class CpraToSpraGrch37Converter:
    """Convert Cpra to Spra for GRCh37."""

    chrom_ac_mapper = chrom_ac_mapper_grch37

    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def convert(self, cpra: Cpra) -> Spra:
        ac = self.chrom_ac_mapper.chrom_to_ac(chrom=cpra.chrom)
        spra = Spra(ac=ac, pos=cpra.pos, ref=cpra.ref, alt=cpra.alt)
        return spra
