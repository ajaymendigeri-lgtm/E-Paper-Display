cd ~
cat > show_photo.py << 'PY'
#!/usr/bin/env python3
import sys, os
from PIL import Image
import epaper

# try common 7.5" driver names (tri-color / variants)
MODELS = ['epd7in5b_V2','epd7in5_V2','epd7in5_HD','epd7in5b_HD','epd7in5bc','epd7in5']

epd = None
model_used = None
for m in MODELS:
    try:
        lib = epaper.epaper(m)
        epd = lib.EPD()
        model_used = m
        break
    except Exception:
        continue

if epd is None:
    print("No supported e-paper driver found. Make sure 'waveshare-epaper' is installed or clone the waveshare repo.")
    sys.exit(2)

print("Using driver:", model_used)
epd.init()
epd.Clear()

# determine the photo path: optional CLI arg, otherwise look in common places
if len(sys.argv) > 1:
    photo = sys.argv[1]
else:
    candidates = [os.path.expanduser('~/Pictures/photo.jpg'),
                  os.path.expanduser('~/photo.jpg'),
                  os.path.expanduser('~/images/photo.jpg'),
                  os.path.expanduser('~/Image/photo.jpg')]
    found = None
    for c in candidates:
        if os.path.exists(c):
            found = c
            break
    if not found:
        # try a quick search (home, shallow)
        try:
            out = os.popen("find ~ -maxdepth 3 -type f -iname 'photo.jpg'").read().strip()
            if out:
                found = out.splitlines()[0]
        except Exception:
            pass
    if not found:
        print("photo.jpg not found. Run: python3 show_photo.py /path/to/photo.jpg")
        epd.sleep()
        sys.exit(3)
    photo = found

print("Loading:", photo)
img = Image.open(photo).convert('RGB')

# get display size from driver (most Waveshare drivers expose .width/.height)
w, h = getattr(epd, 'width', None), getattr(epd, 'height', None)
if not w or not h:
    print("Couldn't read display resolution from driver. Exiting.")
    epd.sleep()
    sys.exit(4)

img = img.resize((w, h))
black = Image.new('1', (w, h), 255)  # white background
red   = Image.new('1', (w, h), 255)

px = img.load()
bpx = black.load()
rpx = red.load()

# basic color separation:
for y in range(h):
    for x in range(w):
        r,g,b = px[x,y]
        # simple red-detection heuristic
        if r > 160 and r > g + 30 and r > b + 30:
            rpx[x,y] = 0   # mark red pixel
            bpx[x,y] = 255
        else:
            lum = 0.299*r + 0.587*g + 0.114*b
            bpx[x,y] = 0 if lum < 128 else 255

# send to display (black buffer, red buffer)
try:
    epd.display(epd.getbuffer(black), epd.getbuffer(red))
except TypeError:
    # some drivers accept single-buffer displays
    epd.display(epd.getbuffer(black))
epd.sleep()
print("Done.")
PY

# make it executable
chmod +x show_photo.py