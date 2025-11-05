cat > ~/clear_display.py <<'PY'
#!/usr/bin/env python3
from waveshare_epd import epd7in5b_V2

epd = epd7in5b_V2.EPD()
epd.init()
epd.Clear()     # fill with white
epd.sleep()     # low-power mode
print("Display cleared and put to sleep.")
PY

chmod +x ~/clear_display.py
sudo python3 ~/clear_display.py
