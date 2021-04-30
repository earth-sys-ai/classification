import datetime
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from spatialist import vector
import shutil
import os
import pyroSAR
from pyroSAR.snap import geocode
import sys

# authorize api
with open('secrets', 'r') as file:
    raw = file.readlines()
api = SentinelAPI(raw[0].strip(), raw[1].strip(), 'https://apihub.copernicus.eu/apihub')

# start date, end date, polygon, outfile -> geotiff
def get_tile(START, END, gjson, out):

    # search database for matching archives
    print('Querying database...')
    footprint = geojson_to_wkt(read_geojson(gjson))
    products = api.query(footprint,
                         ingestiondate=(START, END),
                         platformname='Sentinel-1',
                         producttype='GRD',
                         sensoroperationalmode='IW',
                         orbitdirection='ASCENDING',
                         polarisationmode='VH')

    # download archive
    print('Downloading archive...')
    pmd = api.download_all(products, directory_path='./temp/')
    fname = './temp/' + list(pmd[0].values())[0]['title'] + '.zip'

    # unpack and ingest
    print('Unpacking archive...')
    scene = pyroSAR.identify(fname)
    scene.unpack('./temp/', overwrite=True)

    # geocode
    print('Geocoding data...')
    shp = vector.Vector(filename=gjson)
    geocode(infile=scene, outdir='./temp/', tr=int(sys.argv[3]), scaling='db', removeS1ThermalNoise=True, demResamplingMethod='BISINC_21_POINT_INTERPOLATION',
            terrainFlattening=True, allow_RES_OSV=True, speckleFilter='Refined Lee', shapefile=shp, cleanup=True)

    # save image
    print('Copying image...')
    smd = scene.scanMetadata()
    iname = './temp/' + [file for file in os.listdir('./temp/') if '{}__{}___{}_{}_VH'.format(
        smd['sensor'], smd['acquisition_mode'], smd['orbit'], smd['start']) in file][0]
    shutil.copy2(iname, out)

    # done
    print('Done.')