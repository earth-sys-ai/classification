from bs4 import BeautifulSoup
import geopandas as gpd
import pandas as pd
import numpy as np
import requests
import sys
import os
headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

# get bbox and date range from name
LAT_PAD = 0.25
LON_PAD = 0.75
POS = 4

# get code from name and year
def get_code(year, name):
    url = 'http://www.nhc.noaa.gov/gis/archive_wsurge.php?year='+str(year)
    r = requests.get(url,headers=headers,verify=False)
    soup = BeautifulSoup(r.content, 'lxml')
    table = soup.find('table')
    tab = []
    for row in table.find_all('tr'):
        tmp = row.get_text().strip().split()
        tab.append([tmp[0],tmp[-1]])
    df = pd.DataFrame(
        data=tab[:],
        columns=['identifier', 'name'],
    ).set_index('name')
    hid = df.to_dict()['identifier'][name.upper()]
    return ('{}'+str(year)).format(hid)

# move coord away from center
def magnify(coord, pad):
    return coord - pad

# drops back to zero
def get_index(cats):
    index = cats.idxmax()
    while cats.iat[index] != 0:
        index += 1
    return index

# get bbox from code
def get_data(year, name):
    code = get_code(year, name)
    url   = 'http://www.nhc.noaa.gov/gis/best_track/'
    points = gpd.read_file(
        # (url+'/{}_best_track.zip').format(code),
        'bruh.dbf',
    )

    # get storm touchdown
    index = get_index(points['SS'])
    
    # scrape values
    lat = points['LAT'].iat[index - POS]
    lon = points['LON'].iat[index - POS]
    mon = points['MONTH'].iat[index - POS]
    day = points['DAY'].iat[index - POS]

    # return with equal gap on each side
    return ([magnify(lat, -LAT_PAD), magnify(lon, -LON_PAD)], [magnify(lat, LAT_PAD), magnify(lon, LON_PAD)], mon, day)