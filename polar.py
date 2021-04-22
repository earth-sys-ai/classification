import datetime
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from spatialist import vector
import shutil
import os
import pyroSAR
# import numpy as np
# from PIL import Image
# from osgeo import gdal
from pyroSAR.snap import geocode
import sys

# authorize api
with open('secrets', 'r') as file:
    raw = file.readlines()
api = SentinelAPI(raw[0].strip(), raw[1].strip())


# start date, end date, polygon, outfile -> geotiff
def get_tile(START, END, gjson, out):

    # download raw data
    footprint = geojson_to_wkt(read_geojson(gjson))
    products = api.query(footprint,
                         ingestiondate=(START, END),
                         platformname='Sentinel-1',
                         producttype='GRD',
                         sensoroperationalmode='IW',
                         orbitdirection='ASCENDING',
                         polarisationmode='VH')
    pmd = api.download_all(products, directory_path='./temp/')
    fname = list(pmd[0].values())[0]['path']

    # unpack and ingest
    scene = pyroSAR.identify(fname)
    scene.unpack('./temp/', overwrite=True)

    # geocode
    shp = vector.Vector(filename=gjson)
    geocode(infile=scene, outdir='./temp/', tr=int(sys.argv[3]), scaling='db',
            removeS1ThermalNoise=True, terrainFlattening=False, allow_RES_OSV=True, speckleFilter='Refined Lee', shapefile=shp)

    # save image
    smd = scene.scanMetadata()
    iname = './temp/{}__{}___{}_{}_VH_NR_Orb_Cal_TC_dB.tif'.format(
        smd['sensor'], smd['acquisition_mode'], smd['orbit'], smd['start'])
    shutil.copy2(iname, out)


# before
get_tile(datetime.datetime(2021, 2, 28), datetime.datetime(
    2021, 3, 4), sys.argv[1], sys.argv[2])

# after
# get_tile(datetime.datetime(2020, 8, 28), datetime.datetime(2020, 9, 4))

# convert to png`
# ds = gdal.Open('./pics/S1A__IW___A_20210228T001841_VH_NR_Orb_Cal_TC_dB.tif', gdal.GA_ReadOnly)
# band = ds.GetRasterBand(1).ReadAsArray()
# band = np.interp(band, (np.amin(band), np.amax(band)), (0, 255)).astype('uint8')
# img = Image.fromarray(band)
# img.save('./pics/test.png')
