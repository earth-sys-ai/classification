import geemap
import ee
ee.Initialize()

START = "2017-08-25"
END = "2017-09-25"

ivp = {"opacity":1,"bands":["VV","VH","VV/VH"],"min":-20,"max":-5,"gamma":5};

date_start = ee.Date(START)
date_end = ee.Date(END)

def img_map(image):
  edge = image.lt(-50.0)
  maskedImage = image.mask().And(edge.Not())
  return image.updateMask(maskedImage)

ic_vvvh = (ee.ImageCollection('COPERNICUS/S1_GRD')
        .filterDate(date_start,date_end)
        .filterMetadata("transmitterReceiverPolarisation","equals",["VV","VH"])
        .filter(ee.Filter.eq('instrumentMode', 'IW'))
        .map(img_map))

def add_ratio_band(image):
  new_image = ee.Image(image)
  i_ratio = image.select("VV").divide(image.select("VH"))
  i_ratio = i_ratio.rename("VV/VH")
  new_image = new_image.addBands(i_ratio)
  return new_image

def add_difference_band(image):
  new_image = ee.Image(image)
  i_ratio = image.select("VV").subtract(image.select("VH"))
  i_ratio = i_ratio.rename("VV-VH")
  new_image = new_image.addBands(i_ratio)
  return new_image

ic_vvvh = ic_vvvh.map(add_ratio_band)
ic_vvvh = ic_vvvh.map(add_difference_band)

ic_vvvh_desc = ic_vvvh.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))
ic_vvvh_asc = ic_vvvh.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))

Map = geemap.Map()
Map.addLayer(ic_vvvh_asc, ivp, "S1 [VV,HV,VV/HV]")

POLAR_URL = Map.layers[-1].url[:-11]