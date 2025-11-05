cd ~/e-Paper/RaspberryPi_JetsonNano/python

cat > display_image.py <<'PY'
#!/usr/bin/env python3
import os, sys
from PIL import Image

# make sure the local waveshare lib is importable
libdir = os.path.join(os.path.dirname(_file_), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

# try the common 7.5" driver import name
try:
    from waveshare_epd import epd7in5_V2 as epd_mod
except Exception:
    try:
        import epd7in5_V2 as epd_mod
    except Exception:
        print("Could not import a 7.5in driver. Check that e-Paper/python/lib is present.")
        sys.exit(1)

epd = epd_mod.EPD()

if len(sys.argv) < 2:
    print("Usage: python3 display_image.py /path/to/image.jpg")
    sys.exit(1)

img_path = sys.argv[1]
if not os.path.exists(img_path):
    print("Image file not found:", img_path); sys.exit(1)

# init & clear
epd.init()
try:
    epd.Clear()
except Exception:
    pass

# load image, convert & resize to panel resolution
w, h = epd.width, epd.height
print("EPD resolution:", w, "x", h)
img = Image.open(img_path).convert('RGB')
img = img.resize((w, h))
# convert to 1-bit (monochrome); for tri-color modules this step may vary
img_bw = img.convert('1')

# send to display (use driver's helper if present)
try:
    buf = epd.getbuffer(img_bw)
    epd.display(buf)
except Exception:
    try:
        epd.display(img_bw)
    except Exception as e:
        print("Failed to display image:", e)
        sys.exit(1)

epd.sleep()
print("Done: image sent to e-paper")
PY

chmod +x display_image.py
