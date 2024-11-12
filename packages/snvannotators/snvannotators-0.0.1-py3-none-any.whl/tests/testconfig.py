"""Config for SNV annotator module."""

import gzip
import json
from pathlib import Path
from typing import Optional


# Read JSON file gzipped or not
def read_json(json_file, hook: callable = None, verbose=False) -> dict:
    """Read JSON file gzipped or not into Python dict.

    Args:
        json_file (str): path of a JSON file.
        verbose (bool, optional): verbose or not. Defaults to False.

    Raises:
        ValueError: if its suffix is not json or gz.

    Returns:
        dict: a dict for the JSON.
    """
    suffixes = Path(json_file).suffixes
    if suffixes[-1] == ".json":
        if verbose:
            print("Input JSON file")
        with open(json_file, "r", encoding="utf-8") as fin:
            json_str = fin.read()
    elif suffixes[-2] == ".json" and suffixes[-1] == ".gz":
        if verbose:
            print("Input gzipped file")
        with gzip.open(json_file, "r") as fin:
            json_bytes = fin.read()
        json_str = json_bytes.decode("utf-8")
    else:
        raise ValueError("Wrong file suffix: either json or json.gz")
    if hook is None:
        json_dict = json.loads(json_str)
    else:
        json_dict = json.loads(json_str, object_hook=hook)
    if verbose:
        print("Read JSON completed")
    return json_dict


class TestConfig:
    """Config for testing."""

    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(
        self,
        config_file: Optional[Path] = Path("test_config.json"),
        verbose: bool = False,
    ):
        self.config_file = Path(__file__).resolve().parent / config_file
        self.verbose = verbose
        self.data = self.read_config_file()

    def read_config_file(self, hook: callable = None) -> dict:
        """Read config file

        Args:
            hook (callable, optional): hook for json.loads(). Defaults to None.

        Returns:
            dict: config information.
        """
        return read_json(self.config_file, hook=hook, verbose=self.verbose)

    def get_oncokb_authorization(self) -> str:
        """Get OncoKB authorization."""
        return self.data["oncokb_authorization"]
