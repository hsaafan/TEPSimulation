global VIEWPORT_WIDTH, VIEWPORT_HEIGHT, WINDOW, REFRESH_RATE
global AXRNG, AXRNG_DEFAULT, AXRNG_MIN, AXRNG_MAX
global XOFFSET, YOFFSET
global PROJECTION_COORDS

VIEWPORT_WIDTH = 500
VIEWPORT_HEIGHT = 500
REFRESH_RATE = 30
AXRNG_DEFAULT = 4.0
AXRNG_MIN = 2.0
AXRNG_MAX = 10.0
COLORS_RGB = {
    'black':    (0.0, 0.0, 0.0),
    'red':      (1.0, 0.0, 0.0),
    'green':    (0.0, 1.0, 0.0),
    'blue':     (0.0, 0.0, 1.0),
    'yellow':   (1.0, 1.0, 0.0),
    'cyan':     (0.0, 1.0, 1.0),
    'magenta':  (1.0, 0.0, 1.0),
    'white':    (1.0, 1.0, 1.0),
}
COLORS_RGBA = {key: (*value, 1.0) for (key, value) in COLORS_RGB.items()}
