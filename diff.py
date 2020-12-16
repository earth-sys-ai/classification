from PIL import Image, ImageFilter, ImageChops
import sys

# parameters
Image.MAX_IMAGE_PIXELS = None
FIRST = sys.argv[1]
SECOND = sys.argv[2]
OUT = sys.argv[3]
MIN = 190

# load and apply
img1 = Image.open(FIRST).convert('L')
img2 = Image.open(SECOND).convert('L')
con = ImageChops.subtract(img1, img2)
out = con.point(lambda p: (p >= MIN) * 255)
out.filter(ImageFilter.FIND_EDGES).save(OUT)