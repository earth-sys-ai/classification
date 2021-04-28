from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np


def find_difference(after, before, outname):
    ds1 = gdal.Open(after, gdal.GA_ReadOnly)
    band_a = ds1.GetRasterBand(1).ReadAsArray().astype('bool')

    ds2 = gdal.Open(before, gdal.GA_ReadOnly)
    band_b = ds2.GetRasterBand(1).ReadAsArray().astype('bool')

    band_b = np.resize(band_b, band_a.shape)

    diff = band_a & ~band_b

    driver = ds1.GetDriver()
    out = driver.CreateCopy(outname, ds1, 0)
    out.GetRasterBand(1).WriteArray(band_b)
    out.FlushCache()
