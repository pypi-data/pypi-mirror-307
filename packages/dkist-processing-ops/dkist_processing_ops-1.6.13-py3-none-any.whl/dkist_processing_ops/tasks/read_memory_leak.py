from abc import ABC
from pathlib import Path

import numpy as np
from astropy.io import fits
from dkist_processing_common.codecs.fits import fits_hdu_decoder
from dkist_processing_common.codecs.path import path_decoder
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks import WorkflowTaskBase


def generated_hdu_decoder(path: Path) -> fits.PrimaryHDU | fits.CompImageHDU:
    data = np.random.rand(4096, 4096)
    hdu = fits.CompImageHDU(data)
    return hdu


class FitsDataRead(WorkflowTaskBase, ABC):
    @property
    def run_type(self):
        return self.metadata_store_recipe_run_configuration().get("run_type", "file_read")

    def run(self) -> None:
        if self.run_type == "file_read":
            hdus = self.read(tags=[Tag.input(), Tag.frame()], decoder=fits_hdu_decoder)
            for hdu in hdus:
                h = hdu.header
                d = hdu.data

        if self.run_type == "generated_read":
            hdus = self.read(tags=[Tag.input(), Tag.frame()], decoder=generated_hdu_decoder)
            for hdu in hdus:
                h = hdu.header
                d = hdu.data

        if self.run_type == "file_task":
            filepaths = self.read(tags=[Tag.input(), Tag.frame()], decoder=path_decoder)
            for filepath in filepaths:
                hdu = fits.open(filepath)[1]
                h = hdu.header
                d = hdu.data

        if self.run_type == "generated_task":
            filepaths = self.read(tags=[Tag.input(), Tag.frame()], decoder=path_decoder)
            for filepath in filepaths:
                data = np.random.rand(4096, 4096)
                hdu = fits.CompImageHDU(data)
                h = hdu.header
                d = hdu.data
