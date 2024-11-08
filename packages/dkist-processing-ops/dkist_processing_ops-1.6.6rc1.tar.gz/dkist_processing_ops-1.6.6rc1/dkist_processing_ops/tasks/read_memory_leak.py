from abc import ABC
from pathlib import Path

import numpy as np
from astropy.io import fits
from dkist_processing_common.codecs.fits import fits_hdu_decoder
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks import WorkflowTaskBase


def _extract_hdu(hdul: fits.HDUList) -> fits.PrimaryHDU | fits.CompImageHDU:
    """Return the fits hdu associated with the data in the hdu list."""
    if hdul[0].data is not None:
        return hdul[0]
    return hdul[1]


def fits_hdu_decoder_with_close(path: Path) -> fits.PrimaryHDU | fits.CompImageHDU:
    """Read a Path with `fits` to produce an `HDUList`."""
    hdu_list = fits.open(path, memmap=False)
    hdu_to_return = _extract_hdu(hdu_list).copy()
    hdu_list.close()
    return hdu_to_return


def fits_hdu_decoder_with_close_and_del(path: Path) -> fits.PrimaryHDU | fits.CompImageHDU:
    """Read a Path with `fits` to produce an `HDUList`."""
    hdu_list = fits.open(path, memmap=False)
    hdu_to_return = _extract_hdu(hdu_list).copy()
    hdu_list.close()
    del hdu_list
    return hdu_to_return


class FitsDataRead(WorkflowTaskBase, ABC):
    @property
    def fits_data_read_strategy(self) -> str:
        """Recipe run configuration indicating how fFITS data should be read."""
        return self.metadata_store_recipe_run_configuration().get(
            "fits_data_read_strategy", "leave_open"
        )

    def run(self) -> None:
        if self.fits_data_read_strategy == "leave_open":
            hdus = self.read(tags=[Tag.input(), Tag.frame()], decoder=fits_hdu_decoder)
        if self.fits_data_read_strategy == "close":
            hdus = self.read(tags=[Tag.input(), Tag.frame()], decoder=fits_hdu_decoder_with_close)
        if self.fits_data_read_strategy == "close_and_del":
            hdus = self.read(
                tags=[Tag.input(), Tag.frame()], decoder=fits_hdu_decoder_with_close_and_del
            )
        for hdu in hdus:
            data = hdu.data
            header = hdu.header
            total = np.sum(data)
