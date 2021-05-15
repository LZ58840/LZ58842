import re

RESOLUTION_ANY = r"[(\[]([0-9]{3,})\s?[Xx×]\s?([0-9]{4,})[)\]]"
MOBILE_W, MOBILE_H = 900, 1600
DESKTOP_W, DESKTOP_H = 1920, 1080
RESOLUTION_MIN = {"Mobile": [MOBILE_W, MOBILE_H], "Desktop": [DESKTOP_W, DESKTOP_H]}
ASPECT_RATIO = {"Mobile": 0.625, "Desktop": 1.6}
