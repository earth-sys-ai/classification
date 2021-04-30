import datetime
import polar
import delta
import classify
import sys

# get before VH
polar.get_tile(datetime.datetime(2021, 4, 6), datetime.datetime(
    2021, 4, 12), sys.argv[1], './temp/r_before.tif')

# get after VH
polar.get_tile(datetime.datetime(2021, 4, 20), datetime.datetime(
    2021, 4, 26), sys.argv[1], './temp/r_after.tif')

# classify water before
classify.detect_water('./temp/r_before.tif', './temp/w_before.tif')

# classify water after
classify.detect_water('./temp/r_after.tif', './temp/w_after.tif', contour=True)

# subtract
delta.find_difference('./temp/w_before.tif', './temp/w_after.tif', sys.argv[2])
