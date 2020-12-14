from PIL import Image, ImageFilter, ImageChops
import sys

# parameters
Image.MAX_IMAGE_PIXELS = None
FIRST = sys.argv[1]
SECOND = sys.argv[2]
OUT = sys.argv[3]
FIL = 1

# load and apply
img1 = Image.open(FIRST).convert('L').filter(ImageFilter.MinFilter(FIL))
img2 = Image.open(SECOND).convert('L').filter(ImageFilter.MinFilter(FIL))
ImageChops.subtract(img2, img1).save(OUT)