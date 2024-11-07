"""Create ChromAcMapper for NCBI genome assembly."""

import csv
import logging
from pathlib import Path

from appdirs import user_data_dir
import requests

from ..chromacmapper import ChromAcMapper

logger = logging.getLogger(__name__)


class NcbiChromAcMapperCreator:
    """Create ChromAcMapper for NCBI genome assembly.
    
    Example URL: https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.25_GRCh37.p13/GCF_000001405.25_GRCh37.p13_assembly_report.txt
    """
    def __init__(self, url: str):
        self.url = url
        
    def create(self) -> ChromAcMapper:
        local_data_file = self.get_local_data_file()
        chroms = []
        acs = []
        with open(local_data_file, "r") as fh:
            reader = csv.reader(fh, delimiter="\t")
            for row in reader:
                if row[0].startswith("#"):
                    continue
                if row[7] == "Primary Assembly":
                    acs.append(row[6])
                    chroms.append(row[9])
        chrom_ac_mapper = ChromAcMapper(chroms=chroms, acs=acs)
        return chrom_ac_mapper

    def get_local_data_file(self) -> Path:
        # Get the platform-specific user data directory (e.g., ~/.my_package)
        data_dir = Path(user_data_dir('snvmodels'))
        data_dir.mkdir(exist_ok=True)
        file_name = self.get_file_name()
        local_data_file = data_dir / file_name
        if not local_data_file.exists():
            logger.debug("Download %s", self.url)
            self.download_file(local_data_file=local_data_file)
            logger.debug("Download is done. Save as %s", local_data_file)
        else:
            logger.debug("File exists %s", local_data_file)
        return local_data_file
    
    def download_file(self, local_data_file: Path):
        response = requests.get(self.url)
        response.raise_for_status()  # Ensure we catch download errors
        with open(local_data_file, 'wb') as f:
            f.write(response.content)
            
    def get_file_name(self) -> str:
        return Path(self.url).name
