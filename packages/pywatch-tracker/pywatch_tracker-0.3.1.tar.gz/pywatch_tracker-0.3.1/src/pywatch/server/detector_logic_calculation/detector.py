import json
import typing
import warnings
from dataclasses import dataclass, field

import numpy as np

from .vector import euler_order, Vector


__all__ = ["DETECTOR_HEIGHT", "DETECTOR_WIDTH", "Interval", "get_sections", "intersect", "line_in_cuboid",
           "Line", "Detector", "detector", "load_detectors_from_file"]

DETECTOR_WIDTH = 5
DETECTOR_HEIGHT = 1

Interval = typing.Tuple[float, float]


def get_sections(segmentation: int) -> typing.List[Vector]:
    width = DETECTOR_WIDTH / segmentation
    sectors = []

    if segmentation % 2 == 1:
        max_index = int((segmentation - 1) / 2)
        coord = [width * i for i in range(-max_index, max_index + 1)]
        for x in coord:
            for z in coord:
                sectors.append(Vector(x, 0.8, z))

        return sectors
    else:
        raise NotImplementedError


def intersect(i1: Interval, i2: Interval) -> typing.Optional[Interval]:
    """Calculate the intersection between two intervals. None represents the empty set"""
    min_ = max(i1[0], i2[0])
    max_ = min(i1[1], i2[1])

    if max_ <= min_:
        return None

    return min_, max_


def line_in_cuboid(v1: Vector, v2: Vector, center: Vector, width: float, height: float) -> bool:
    r = v2 - v1
    s = center - v1
    b = Vector(width, height, width)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # intervals = [sorted((np.true_divide((s_ - b_), r_), np.true_divide((s_ + b_), r_))) for r_, s_, b_ in
        #              zip(r, s, b)]
        intervals = []
        for s_, b_, r_ in zip(s, b, r):
            if r_ == 0 and (s_ < - b_ / 2 or s_ > b_ / 2):
                return False

            intervals.append(sorted((np.true_divide((s_ - b_ / 2), r_), np.true_divide((s_ + b_ / 2), r_))))

    i = intersect(intervals[0], intervals[1])
    if i is None:
        return False

    i = intersect(i, intervals[2])

    return bool(i)

    #
    # if abs(k.x) > width / 2 or abs(k.y) > height / 2 or abs(k.z) > width / 2:
    #     return False


class Line:
    def __init__(self, v1: Vector, v2: Vector):
        r = v2 - v1
        if r.y > 0:
            r *= -1
        elif r.y == 0:
            if r.z < 0:
                r *= -1

        self.position = v1
        self.direction = r


@dataclass
class Detector:
    segmentation: int
    position: Vector
    rotation: (euler_order, Vector) = ("yxz", Vector())
    sections: typing.List[Vector] = field(init=False, default_factory=list, repr=False)
    section_width: float = field(init=False)

    def __post_init__(self):
        for vector in get_sections(self.segmentation):
            self.sections.append(vector + self.position)

        self.section_width = DETECTOR_WIDTH / self.segmentation

    def line_in_detector(self, line: Line) -> bool:
        # rotate line
        v1 = line.position
        v2 = line.position + line.direction

        order = self.rotation[0][::-1]
        angle = Vector(*list(self.rotation[1] * -1)[::-1])

        v1 = v1.rotate(order, angle)
        v2 = v2.rotate(order, angle)

        line = Line(v1, v2)

        # for center in self.sections:
        #     if line_in_cuboid(line.position, line.position + line.direction, center,
        #                       self.section_width, DETECTOR_HEIGHT):
        #         return True

        return line_in_cuboid(line.position, line.position + line.direction,
                              self.position, DETECTOR_WIDTH, DETECTOR_HEIGHT)


def detector(segmentation: int, dt: dict) -> Detector:
    position = Vector(*dt["position"])
    rotation = dt.get("rotation", [0, 0, 0, "XYZ"])
    rotation = (rotation[3], Vector(*rotation[:3]))

    return Detector(segmentation, position, rotation)


def load_detectors_from_file(file_path: str, segmentation: int) -> typing.List[Detector]:
    with open(file_path, "r") as f:
        detectors_raw = json.load(f)["detectors"]

    detectors = [detector(segmentation, dct) for dct in detectors_raw]

    return detectors
