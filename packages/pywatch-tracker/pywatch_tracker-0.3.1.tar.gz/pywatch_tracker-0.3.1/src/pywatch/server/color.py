import typing
from dataclasses import dataclass

from colour import Color


__all__ = ["ColorRange", "Color"]


def color_to_hex(color: Color) -> str:
    red = int(round(color.get_red() * 255, 0))
    green = int(round(color.get_green() * 255, 0))
    blue = int(round(color.get_blue() * 255, 0))

    res = "0x"
    for n in [red, green, blue]:
        res += "{:02X}".format(n)

    return res


@dataclass
class ColorRange:
    min: float
    max: float
    color1: Color
    color2: Color
    func: typing.Callable[[float], float] = lambda x: x

    def __post_init__(self):
        self.range = list(self.color1.range_to(self.color2, 1000))

    def __call__(self, value: float) -> str:
        if value < self.min:
            return color_to_hex(self.color1)
        if value > self.max:
            return color_to_hex(self.color2)

        value -= self.min
        value /= (self.max - self.min)
        return color_to_hex(self.range[int(value * 999)])
