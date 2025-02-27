import os
import pytest
from astropy.io import fits
import simcado as sim

if "USERNAME" in os.environ and os.environ["USERNAME"] == "Kieran":
    sim.__search_path__.insert(0, "C:\Work\irdb\_Legacy_packages\MICADO")


class TestTravisDownloadsGetExtras:
    def test_find_psf_file_with_find_file(self):
        filename = "PSF_SCAO.fits"
        filepath = sim.utils.find_file(filename)

        print(filepath, sim.__search_path__)
        assert os.path.exists(filepath) is not None


class TestBasicUseCases:
    def test_simple_run(self):
        src = sim.source.cluster()
        hdu = sim.run(src, OBS_DIT=3600, SCOPE_PSF_FILE="PSF_MCAO.fits",
                      filter_name="J", mode="zoom")
        assert isinstance(hdu, fits.HDUList)
