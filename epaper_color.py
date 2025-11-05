#!/usr/bin/env python3
import sys
import os
from PIL import Image
from waveshare_epd import epd7in5b_V2  # driver for 7.5" b/w/r V2

epd = epd7in5b_V2.EPD()
epd.init()
epd.Clear()

# get photo path
if len(sys.argv) > 1:
    photo = sys.argv[1]
else:
    photo = os.path.expanduser("~/Pictures/photo.jpg")

print("Loading:", photo)
img = Image.open(photo).convert("RGB")

# resize to fit
img = img.resize((epd.height, epd.width))  # note: waveshare drivers swap width/height

black = Image.new("1", (epd.height, epd.width), 255)
red   = Image.new("1", (epd.height, epd.width), 255)

px = img.load()
bpx = black.load()
rpx = red.load()

for y in range(epd.width):
    for x in range(epd.height):
        r, g, b = px[x, y]
        if r > 160 and r > g + 30 and r > b + 30:
            rpx[x, y] = 0
        else:
            lum = 0.299 * r + 0.587 * g + 0.114 * b
            bpx[x, y] = 0 if lum < 128 else 255

epd.display(epd.getbuffer(black), epd.getbuffer(red))
epd.sleep()
