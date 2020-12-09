from PIL import Image, ImageFilter, ImageChops
import sys

# parameters
Image.MAX_IMAGE_PIXELS = None
RAD = sys.argv[1]
VIS = sys.argv[2]
OUT = sys.argv[3]
MAX = 100
FIL = 1

# load and apply
print('Loading images...')
img = Image.open(RAD).convert('L').point(lambda p: (p < MAX) * 255)
out = Image.open(VIS)
print('Applying mask...')
mask = ImageChops.darker(out.getchannel('A'), img.filter(ImageFilter.MinFilter(FIL))) 
out.putalpha(mask)
print('Writing image...')
out.save(OUT)