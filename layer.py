import math
import sys
import tqdm
import requests
from PIL import Image
from io import BytesIO

SIZE = 256

# download tile with any available links 
def downloadTile(xtile, ytile, zoom, urls):
    imgs = []
    for url in urls:
        link = url + str(zoom) + '/' + str(xtile) + '/' + str(ytile)
        resp = requests.get(link)
        if resp.status_code != 404:            
            img = Image.open(BytesIO(resp.content))
            imgs.append(img.convert('RGBA'))
    return imgs

# black magic
def getTileURL(lat, lon, zoom):
    xtile = int(math.floor( (lon + 180) / 360 * (1 << zoom) ))
    ytile = int(math.floor( (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * (1 << zoom) ))
    return [xtile, ytile]

# download all the tiles within the given coords
def downloadTiles(scoord, ecoord, zoom, urls, file, pos):
    
    start = getTileURL(scoord[0], scoord[1], zoom)
    stop = getTileURL(ecoord[0], ecoord[1], zoom)

    if start[0] > stop[0]:
        start[0], stop[0] = stop[0], start[0]
    if start[1] > stop[1]:
        start[1], stop[1] = stop[1], start[1]

    width = SIZE * (stop[0] - start[0])
    height = SIZE * (stop[1] - start[1])
    tilecount = (stop[0] - start[0]) * (stop[1] - start[1])

    outp = Image.new('RGBA', (width, height))
    with tqdm.tqdm(total = tilecount, position = pos, desc = file) as bar:

        total = 0
        for xtile in range(start[0], stop[0]):
            for ytile in range(start[1], stop[1]):

                imgs = downloadTile(xtile, ytile, zoom, urls)

                for img in imgs:
                    if img != None:
                        xoff = (xtile - start[0]) * SIZE
                        yoff = (ytile - start[1]) * SIZE

                        outp.paste(img, (xoff, yoff), mask = img)
                        img.close()

                total += 1
                bar.update(total)

    outp.save(file)

