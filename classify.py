from skimage import feature, measure, morphology
import matplotlib.pyplot as plt
from osgeo import gdal
import numpy as np

# parameters
t_min = -49
t_max = -21
s_min = 1000


def detect_water(fname, outname, contour=False):

    # read image
    ds = gdal.Open(fname, gdal.GA_ReadOnly)
    band = ds.GetRasterBand(1).ReadAsArray()

    # apply threshold
    ct = (band >= t_min) & (band <= t_max)

    # noise removal
    ct = morphology.remove_small_objects(ct, min_size=s_min)
    ct = morphology.binary_dilation(ct)

    # write back to geotiff
    driver = ds.GetDriver()
    out = driver.CreateCopy(outname, ds, 0)
    out.GetRasterBand(1).WriteArray(ct)
    out.FlushCache()

    # contour
    if contour:
        contours = measure.find_contours(ct, fully_connected='high')
        for c in contours:
            plt.plot(c[:, 1], c[:, 0], linewidth=1, color='darkred')
        plt.imshow(band, cmap='gray')
        plt.savefig('./temp/test.png')
