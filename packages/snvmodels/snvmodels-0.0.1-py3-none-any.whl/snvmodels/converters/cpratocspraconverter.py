"""Convert Cpra to Spra."""

from snvmodels.chromacmapper import ChromAcMapper
from snvmodels.cpra import Cpra
from snvmodels.spra import Cspra


class CpraToCspraConverter:

    def __init__(self, chrom_ac_mapper: ChromAcMapper):
        self.chrom_ac_mapper = chrom_ac_mapper

    def convert(self, cpra: Cpra) -> Cspra:
        ac = self.chrom_ac_mapper.chrom_to_ac(chrom=cpra.chrom)
        cspra = Cspra(chrom=cpra.chrom, ac=ac, pos=cpra.pos, ref=cpra.ref, alt=cpra.alt)
        return cspra
