import logging
import os
import sys
from abc import ABC
from pathlib import Path
from typing import Any
from typing import Generator

import numpy as np
from astropy.io import fits
from dkist_processing_common.codecs.path import path_decoder
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks import tag_type_hint
from dkist_processing_common.tasks import WorkflowTaskBase


def yield_from_read(
    self, tags: tag_type_hint, decoder: callable = path_decoder, **decoder_kwargs
) -> Generator[Any, None, None]:
    yield from (decoder(p, **decoder_kwargs) for p in self.scratch.find_all(tags=tags))


def binary_decoder(path: Path) -> bytes:
    """Generates a random blob of binary data."""
    data = os.urandom(67109008)  # This is the size of the VBI data arrays, in bytes
    logging.info(f"Size of data: {sys.getsizeof(data)}")
    logging.info(f"Bytes of data: {len(data)}")
    return data


def fits_smart_hdu_decoder(path: Path) -> fits.PrimaryHDU | fits.CompImageHDU:
    """Read a Path with `fits` to produce an `HDUList`."""
    hdu_list = fits.open(path, lazy_load_hdus=False)
    return hdu_list[1]


class FitsDataRead(WorkflowTaskBase, ABC):
    @property
    def data_type(self) -> str:
        """Recipe run configuration indicating how fFITS data should be read."""
        return self.metadata_store_recipe_run_configuration().get("data_type", "fits")

    @property
    def read_method(self):
        return self.metadata_store_recipe_run_configuration().get("read_method", "return")

    @property
    def manipulate_data(self):
        return self.metadata_store_recipe_run_configuration().get("manipulate_data", True)

    def run(self) -> None:
        if self.data_type == "fits":
            if self.read_method == "return":
                hdus = self.read(tags=[Tag.input(), Tag.frame()], decoder=fits_smart_hdu_decoder)
                for hdu in hdus:
                    h = hdu.header
                    d = hdu.data
                    if self.manipulate_data:
                        total = np.sum(d)
            if self.read_method == "yield":
                hdus = yield_from_read(
                    self, tags=[Tag.input(), Tag.frame()], decoder=fits_smart_hdu_decoder
                )
                for hdu in hdus:
                    h = hdu.header
                    d = hdu.data
                    if self.manipulate_data:
                        total = np.sum(d)
        if self.data_type == "binary":
            if self.read_method == "return":
                hdus = self.read(tags=[Tag.input(), Tag.frame()], decoder=binary_decoder)
                for hdu in hdus:
                    data = hdu
            if self.read_method == "yield":
                hdus = yield_from_read(
                    self, tags=[Tag.input(), Tag.frame()], decoder=binary_decoder
                )
                for hdu in hdus:
                    data = hdu
