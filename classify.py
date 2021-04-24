from skimage import feature, measure, morphology
import matplotlib.pyplot as plt
from osgeo import gdal
import numpy as np
import sys

# parameters
t_min = -49
t_max = -21
s_min = 1000

# read image
ds = gdal.Open(sys.argv[1], gdal.GA_ReadOnly)
band = ds.GetRasterBand(1).ReadAsArray()

# apply threshold
ct = (band >= t_min) & (band <= t_max)

# noise removal
ct = morphology.remove_small_objects(ct, min_size=s_min)
ct = morphology.binary_dilation(ct)

# write back to geotiff
driver = ds.GetDriver()
out = driver.CreateCopy(sys.argv[2], ds, 0)
out.GetRasterBand(1).WriteArray(ct)
out.FlushCache()

# contour
contours = measure.find_contours(ct, fully_connected='high')
for c in contours:
    plt.plot(c[:, 1], c[:, 0], linewidth=1, color='darkred')
plt.imshow(band, cmap='gray')
plt.savefig('pics/test.png')
