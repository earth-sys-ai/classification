import layer
print('Processing radar data with Earth Engine...')
import polar

# parameters
IMAGE_URLS = [
    'https://stormscdn.ngs.noaa.gov/20170902c-rgb/',
    'https://stormscdn.ngs.noaa.gov/20170903a-rgb/',
    'https://stormscdn.ngs.noaa.gov/20170827-rgb/', 
    'https://stormscdn.ngs.noaa.gov/20170828a-rgb/',
    'https://stormscdn.ngs.noaa.gov/20170828b-rgb/',
    'https://stormscdn.ngs.noaa.gov/20170829a-rgb/',
    'https://stormscdn.ngs.noaa.gov/20170829b-rgb/',
    'https://stormscdn.ngs.noaa.gov/20170830-rgb/', 
    'https://stormscdn.ngs.noaa.gov/20170831a-rgb/',
    'https://stormscdn.ngs.noaa.gov/20170831b-rgb/',
    'https://stormscdn.ngs.noaa.gov/20170901a-rgb/',
    'https://stormscdn.ngs.noaa.gov/20170901b-rgb/',
    'https://stormscdn.ngs.noaa.gov/20170901c-rgb/',
    'https://stormscdn.ngs.noaa.gov/20170902a-rgb/',
    'https://stormscdn.ngs.noaa.gov/20170902b-rgb/',
    'https://stormscdn.ngs.noaa.gov/20170902c-rgb/',
    'https://stormscdn.ngs.noaa.gov/20170903a-rgb/'
]

SCOORD = [30.60, -97.14]
ECOORD = [28.73, -92.46]
ZOOM = 10

print('Converting and merging radar tile images:')
layer.downloadTiles(SCOORD, ECOORD, ZOOM, [polar.POLAR_URL], 'radar.png')

print('\nConverting and merging visible tile images:')
layer.downloadTiles(SCOORD, ECOORD, ZOOM, IMAGE_URLS, 'visible.png')