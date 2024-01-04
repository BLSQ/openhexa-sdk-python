"""Datasets package.

See https://github.com/BLSQ/openhexa/wiki/User-manual#datasets and
https://github.com/BLSQ/openhexa/wiki/Using-the-OpenHEXA-SDK#working-with-datasets for more information about OpenHEXA
dataset.
"""

from .dataset import Dataset, DatasetFile

__all__ = ["Dataset", "DatasetFile"]
