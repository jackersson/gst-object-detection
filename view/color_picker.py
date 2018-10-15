import math

# TODO make human enabled color
v = 1.0
s = 1.0
p = 0.0


def rgbcolor(h, f):
    """Convert a color specified by h-value and f-value to an RGB
    three-tuple."""
    # q = 1 - f
    # t = f
    if h == 0:
        return v, f, p
    elif h == 1:
        return 1 - f, v, p
    elif h == 2:
        return p, v, f
    elif h == 3:
        return p, 1 - f, v
    elif h == 4:
        return f, p, v
    elif h == 5:
        return v, p, 1 - f


def uniquecolors(n):
    """Compute a list of distinct colors, ecah of which is
    represented as an RGB three-tuple"""
    hues = (360.0 / n * i for i in range(n))
    hs = (math.floor(hue / 60) % 6 for hue in hues)
    fs = (hue / 60 - math.floor(hue / 60) for hue in hues)
    return [to_rgb(rgbcolor(h, f)) for h, f in zip(hs, fs)]


def to_rgb(item):
    return list(map(lambda x: int(x * 255), item))


class ColorsIterator(object):
    def __init__(self, colors):
        self._colors = colors
        self._current = 0

    def get(self):
        self._current += 1
        if self._current >= len(self._colors):
            self._current = 0

        return self._colors[self._current]


class ColorPicker(object):

    def __init__(self, n_colors=20):
        self._colors = ColorsIterator(uniquecolors(n_colors))
        self._color_by_id = {}

    def get(self, idx):
        if idx not in self._color_by_id:
            self._color_by_id[idx] = self._colors.get()
        return self._color_by_id[idx]
