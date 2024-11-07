from enum import Enum
import colorsys
import numpy as np
from .math import *


class RGB:
    def __init__(self, r, g, b):
        self.rgb = (r, g, b)
        self.r = r
        self.g = g
        self.b = b
        self._normalized = False

    def __repr__(self):
        return f"({self.r}, {self.g}, {self.b})"

    def normalize(self) -> None:
        self._normalized = True
        self.r /= 255
        self.g /= 255
        self.b /= 255
        self.rgb = (self.r, self.g, self.b)

    def denormalize(self) -> None:
        self._normalized = False
        self.r *= 255
        self.g *= 255
        self.b *= 255
        self.rgb = (self.r, self.g, self.b)

    def complement(self):
        if self._normalized:
            return RGB(1 - self.r, 1 - self.g, 1 - self.b)
        else:
            return RGB(255 - self.r, 255 - self.g, 255 - self.b)

    def adjacent(self, d=30):
        d = d / 360
        h, l, s = colorsys.rgb_to_hls(self.r, self.g, self.b)

        h = [(h + d) % 1 for d in (-d, d)]

        a, b = [RGB(*apply(colorsys.hls_to_rgb(hi, l, s), lambda x: int(round(x * 255)))) for hi in h]
        return a, b

    def toVector(self):
        return Vector3(self.r, self.g, self.b)


class AnsiColor:
    def __init__(self, colorCode: int):
        self.code = f"\033[{colorCode}m"

    @property
    def value(self):
        return self.code


class AnsiRGB:
    def __init__(self, rgb: RGB):
        self.code = f"\u001b[38;2;{rgb.r};{rgb.g};{rgb.b}m"

    @property
    def value(self):
        return self.code


class AnsiRGB_BG:
    def __init__(self, rgb: RGB):
        self.code = f"\u001b[48;2;{rgb.r};{rgb.g};{rgb.b}m"

    @property
    def value(self):
        return self.code


class Colors(Enum):
    BLACK = AnsiColor(30)
    RED = AnsiColor(31).value
    GREEN = AnsiColor(32).value
    YELLOW = AnsiColor(33).value  # orange on some systems
    BLUE = AnsiColor(34).value
    MAGENTA = AnsiColor(35).value
    CYAN = AnsiColor(36).value
    LIGHT_GRAY = AnsiColor(37).value
    DARK_GRAY = AnsiColor(90).value
    BRIGHT_RED = AnsiColor(91).value
    BRIGHT_GREEN = AnsiColor(92).value
    BRIGHT_YELLOW = AnsiColor(93).value
    BRIGHT_BLUE = AnsiColor(94).value
    BRIGHT_MAGENTA = AnsiColor(95).value
    BRIGHT_CYAN = AnsiColor(96).value
    WHITE = AnsiColor(97).value

    RESET = '\033[0m'  # called to return to standard terminal text color


def color(text: str, color: Colors | AnsiColor | AnsiRGB | AnsiRGB_BG, reset: bool = True) -> str:
    if reset:
        text = color.value + text + Colors.RESET.value
    elif not reset:
        text = color.value + text

    return text


# Color Conversions

def gammaToLinear(c: float | int) -> float:
    if c >= 0.04045:
        return pow((c + 0.055) / 1.055, 2.4)
    else:
        return c / 12.92


def linearToGamma(c: float | int) -> float:
    if c >= 0.0031308:
        return 1.055 * pow(c, 1 / 2.4) - 0.055
    else:
        return c * 12.92


def rgbToOKLAB(r: int, g: int, b: int, normalize: bool = False):
    r = gammaToLinear(r / (255 if normalize else 1))
    g = gammaToLinear(g / (255 if normalize else 1))
    b = gammaToLinear(b / (255 if normalize else 1))

    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b

    l, m, s = np.cbrt(l), np.cbrt(m), np.cbrt(s)

    L = l * +0.2104542553 + m * +0.7936177850 + s * -0.0040720468
    a = l * +1.9779984951 + m * -2.4285922050 + s * +0.4505937099
    b = l * +0.0259040371 + m * +0.7827717662 + s * -0.8086757660

    return L, a, b


def okLabToRGB(L: float, a: float, b: float):
    l = (L + a * +0.3963377774 + b * +0.2158037573) ** 3
    m = (L + a * -0.1055613458 + b * -0.0638541728) ** 3
    s = (L + a * -0.0894841775 + b * -1.2914855480) ** 3

    r = l * 4.0767416621 + m * 3.3077115913 + s * 0.2309699292
    g = l * 1.2684380046 + m * 2.6097574011 + s * 0.3413193965
    b = l * 0.0041960863 + m * 0.7034186147 + s * 1.7076147010

    r = 255 * linearToGamma(r)
    g = 255 * linearToGamma(g)
    b = 255 * linearToGamma(b)

    r = clamp(r, 0, 255)
    g = clamp(g, 0, 255)
    b = clamp(b, 0, 255)

    return r, g, b
