import asyncio
import random
import time
import typing
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection

import numpy as np
from numpy.random import normal
from pywatch.readout.event_data_collection import EventData, EventDataCollection
from pywatch import PoolThread
from pywatch.readout.hit_data import HitData
from numpy.random import choice

from .detector_logic_calculation import Line, Detector, Vector


def dist(x):
    return np.cos(x * np.pi / 180) ** 2


def generate_lines(
    count: int,
    x_lim: typing.Tuple[float, float] = (-10, 10),
    z_lim: typing.Tuple[float, float] = (-3, 3)) -> typing.List[Line]:
    angles = np.linspace(-90, 90, 1_000)
    probabilities = dist(angles)
    probabilities /= np.sum(probabilities)

    theta = [choice(angles, p=probabilities) for _ in range(count)]
    phi = [choice(np.linspace(0, 180)) for _ in range(count)]

    x = np.linspace(*x_lim, 1_000)
    x = [choice(x) for _ in range(count)]

    z = np.linspace(*z_lim, 1_000)
    z = [choice(z) for _ in range(count)]

    pos = [Vector(i, 0, j) for i, j in zip(x, z)]
    dir_ = [Vector(np.sin(i) * np.cos(j), -np.cos(i), np.sin(i) * np.sin(j)) for i, j in zip(theta, phi)]

    return [Line(p, p + d) for p, d in zip(pos, dir_)]


def get_indices(detectors, line) -> typing.List[int]:
    indices = []
    for i, detector in enumerate(detectors):
        if detector.line_in_detector(line):
            indices.append(i)

    return indices


def generate_hit_data() -> HitData:
    t = int(time.time() * 1000)
    return HitData(
        t,
        t,
        random.randint(5, 500),
        np.random.normal(40, 30),
        0,
        float(random.randint(200, 300) / 10),
    )


def generate_event_data(indices) -> EventData:
    data = EventData()
    for index in indices:
        data[index] = generate_hit_data()

    return data


angles = np.linspace(-90, 90, 1_000)
phi_angles = np.linspace(0, 360)

probabilities = dist(angles)
probabilities /= np.sum(probabilities)


def generate_line(x_positions, z_positions) -> Line:
    theta = choice(angles, p=probabilities) * np.pi / 180
    phi = choice(phi_angles) * np.pi / 180

    x = choice(x_positions)
    z = choice(z_positions)

    pos = Vector(x, 20, z)
    dir_ = Vector(np.sin(theta) * np.cos(phi), -np.cos(theta), np.sin(theta) * np.sin(phi))

    return Line(pos, pos + dir_)


class SimulationPool:
    """Simulates Data from pywatch events"""
    thread = PoolThread()

    def __init__(self, detectors: typing.List[Detector], expected_wait_time: float = 1, std_dev: float = 0.2):
        # self.detector_count = detector_count
        self.detectors = detectors
        self.expected_wait_time = expected_wait_time
        self.std_dev = std_dev

    async def async_run(
        self, event_count: int,
        callback=None,
        x_lim: typing.Tuple[float, float] = (-10, 10),
        z_lim: typing.Tuple[float, float] = (-3, 3)):
        x_positions = np.linspace(*x_lim, 1_000)
        z_positions = np.linspace(*z_lim, 1_000)

        current_count = 0

        while current_count < event_count:
            line = generate_line(x_positions, z_positions)
            event_data = generate_event_data(get_indices(self.detectors, line))
            if len(event_data) < 2:
                continue

            current_count += 1

            if callback is not None:
                await callback(event_data, self.thread)
            await asyncio.sleep(self.expected_wait_time)

    def run(
        self, event_count: int,
        callback=None,
        x_lim: typing.Tuple[float, float] = (-10, 10),
        z_lim: typing.Tuple[float, float] = (-3, 3)):
        try:
            asyncio.get_running_loop().run_until_complete(self.async_run(event_count, callback, x_lim, z_lim))
        except RuntimeError:
            asyncio.run(self.async_run(event_count, callback, x_lim, z_lim))
