from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
from skimage import morphology
from scipy import ndimage

def find_difference(after, before, outname):
    ds1 = gdal.Open(after, gdal.GA_ReadOnly)
    band_a = ds1.GetRasterBand(1).ReadAsArray().astype('bool')

    ds2 = gdal.Open(before, gdal.GA_ReadOnly)
    band_b = ds2.GetRasterBand(1).ReadAsArray().astype('bool')

    xsize = min(band_a.shape[0], band_b.shape[0])
    ysize = min(band_a.shape[1], band_b.shape[1])

    band_a = band_a[1:xsize, 1:ysize]
    band_b = band_b[1:xsize, 1:ysize]
    
    diff = band_a ^ band_b
    diff = morphology.binary_dilation(diff)

    driver = ds1.GetDriver()
    out = driver.CreateCopy(outname, ds1, 0)
    out.GetRasterBand(1).WriteArray(diff)
    out.FlushCache()
