from PIL import Image, ImageFilter, ImageChops
import sys

# parameters
Image.MAX_IMAGE_PIXELS = None
FIRST = sys.argv[1]
SECOND = sys.argv[2]
OUT = sys.argv[3]
MIN = 164

# load and apply
img1 = Image.open(FIRST).convert('1')
img2 = Image.open(SECOND).convert('1')
con = ImageChops.subtract(img1, img2)
out = con.point(lambda p: (p >= MIN) * 255)
out.filter(ImageFilter.FIND_EDGES).save(OUT)