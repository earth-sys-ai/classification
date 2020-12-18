import layer
import polar
import info
import threading 

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

SCOORD, ECOORD, _, _ = info.get_data(2017, 'harvey')
ZOOM = 8
threads = []

# print('\nConverting and merging visible tile images:')
threads.append(threading.Thread(target = layer.downloadTiles, args = (SCOORD, ECOORD, ZOOM, IMAGE_URLS, 'pics/visible.png', 0)))

# print('Converting and merging radar tile images:')
threads.append(threading.Thread(target = layer.downloadTiles, args = (SCOORD, ECOORD, ZOOM, [polar.get_tile('2017-07-01', '2017-08-01')], 'pics/before.png', 1)))
threads.append(threading.Thread(target = layer.downloadTiles, args = (SCOORD, ECOORD, ZOOM, [polar.get_tile('2017-08-25', '2017-09-25')], 'pics/after.png', 2)))

# do the dew
for t in threads:
    t.start()