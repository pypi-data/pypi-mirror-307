import json
import random
import typing
from collections import defaultdict

from .detector import *
from .vector import *


__all__ = ["Coincidences", "calculate_coincidences", "load_from_json"]


class Coincidences(defaultdict):
    def __init__(self):
        super().__init__(list)

    def __getitem__(self, item: typing.List[int]) -> typing.List[typing.Tuple[Vector, Vector]]:
        item.sort()

        return super().__getitem__(str(item).replace(" ", ""))

    def to_dict(self, mode: typing.Literal["mean", "random"] = "mean") -> typing.Dict[
        int, typing.Tuple[Vector, Vector]]:
        dct = dict()

        for key, item in self.items():
            start_points = [start for start, _ in item]
            directions = [dir_ for _, dir_ in item]

            if mode == "mean":
                start_point_mean = sum(start_points, start=Vector()) / len(start_points)
                direction_mean = sum(directions, start=Vector()) / len(directions)

                dct[key] = (start_point_mean, direction_mean / direction_mean.norm())
            elif mode == "random":
                dct[key] = random.choice(item)

        return dct


def get_course_coincidences(detectors: typing.List[Detector]) -> typing.List[typing.List[int]]:
    n = len(detectors)
    coincidences = []

    for i in range(n):
        for j in range(n):
            if j == i:
                continue

            coincidence_indices = [i, j]
            for k in range(n):
                if k == j or k == i:
                    continue

                # if vectors_on_line(x=detectors[i].position, y=detectors[j].position, z=detectors[k].position,
                #                    radius=2.5):
                #     coincidence_indices.append(k)
                v1 = detectors[i].position
                v2 = detectors[j].position
                v3 = detectors[k].position
                if line_in_cuboid(v1, v2, v3, DETECTOR_WIDTH * 1.5, DETECTOR_HEIGHT):
                    coincidence_indices.append(k)

            coincidences.append(coincidence_indices)

    return coincidences


# TODO use multiprocessing
def calculate_coincidences(detectors: typing.List[Detector], max_depth: int = 3) -> Coincidences:
    coincidences = Coincidences()
    cc = get_course_coincidences(detectors)

    for coin in cc:
        i1, i2 = coin[0:2]
        for s1 in detectors[i1].sections:
            for s2 in detectors[i2].sections:
                indices = [i1, i2]
                line = Line(s1, s2)
                # indices.extend([i for i in coin[2:] if is_on_line(line, detectors[i])])
                # indices.extend([i for i in coin[2:] if detectors[i].line_in_detector(line)])
                for i in coin[2:]:
                    if detectors[i].line_in_detector(line):
                        indices.append(i)
                    if len(indices) == max_depth:
                        break

                coincidences[indices].append((line.position, line.direction))

    return coincidences


def load_from_json(segmentation: int, file_path: str) -> (typing.List[Detector], Coincidences):
    with open(file_path, "r") as file:
        dct = json.load(file)

    if dct.get("detectors") is None:
        raise KeyError(f"{file_path} does not have the detectors key")

    detectors = [detector(segmentation, dt) for dt in dct["detectors"]]
    coincidences = calculate_coincidences(detectors)

    return detectors, coincidences
