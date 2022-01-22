import shutil
from pathlib import Path
from typing import Union

from loguru import logger

from src.data import DATA_DIR
from src.utils.io import read_json


class OrganizeFiles:
    """This class used to organize files in directory by moving files
    into directory based on extention
    """
    def __init__(self):
        ext_dir = read_json(DATA_DIR / "extention.json")
        self.extention_dest = {}
        for des_name, ext_list in ext_dir.items():
            for ext in ext_list:
                self.extention_dest[ext] = des_name

    def __call__(self, directory: Union[Path, str]):
        """Organize files in directory by moving them to sub directory
        based on extention.
        """
        directory = Path(directory)
        # check for directory exist
        if not directory.exists():
            raise FileNotFoundError(f"{directory} does not exist.")

        logger.info(f"Organizing files in {directory} ")
        for file_path in directory.iterdir():

            # ignore directories and hidden files
            if file_path.is_dir() or file_path.name.startswith("."):
                continue

            # move file
            if (file_path.suffix.lower()) in self.extention_dest:
                DES_DIR = directory / self.extention_dest[file_path.suffix.lower()]
            else:
                DES_DIR = directory / "Other"

            DES_DIR.mkdir(exist_ok=True)
            logger.info(f"moving {file_path} to {DES_DIR} ")
            shutil.move(str(file_path), str(DES_DIR))


if __name__ == "__main__":
    org_file = OrganizeFiles()
    org_file("/mnt/c/Users/Ali/Downloads")
    logger.info("Done!")
