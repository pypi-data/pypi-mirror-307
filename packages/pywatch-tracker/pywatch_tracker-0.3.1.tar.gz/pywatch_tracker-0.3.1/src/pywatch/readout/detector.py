"""

Module for reading serial port data of the CosmicWatch Detectors.

Classes:
    :py:class:`Detector`
"""
import asyncio
import time
import typing
from asyncio import StreamReader, StreamWriter
from typing import List, Optional

import serial  # type: ignore
from serial_asyncio import open_serial_connection  # type: ignore

from .hit_data import HitData, parse_hit_data


__all__ = ["Detector"]


class Detector:
    """

    Class for use of the Cosmic Watch Detector.

    :param port: Name of the serial port.
    :param save_data: Specifies whether to save the data accumulated in a list.

    :ivar str port: Name of the serial port.

    Example Usage
        >>> # Create a Detector object, start a measurement for 10 hits and print the result.
        >>> detector = Detector("/dev/ttyUSB0")
        >>> detector.run(10)
        >>>
        >>> for hit in detector:
        >>>     print(hit)

    It reads the data asynchronously to be able to read multiple serial ports at once.
    If necessary the Class can be used with async and await.
        >>> async def main()
        >>>     detector = await Detector("/dev/ttyUSB0").open()
        >>>     for _ in range(10):
        >>>         data = await detector.measurement()
        >>>         print(data)
        >>>
        >>>     await detector.close()

    This code makes the same measurement as above for 10 hits. It can also be used in an
    async context manager:
        >>> async def main():
        >>>     async with Detector("/dev/ttyUSB0") as detector:
        >>>         for _ in range(10):
        >>>             data = await detector.measurement()
        >>>             print(data)
    """

    def __init__(self, port: str, save_data: bool = True) -> None:

        self.port = port
        self._reader: Optional[StreamReader] = None
        self._writer: Optional[StreamWriter] = None

        # list of all registered events by the detector
        # if save_data = false, _events should have length 1 with the data of the last hit
        self._events: List[HitData] = []
        self._start_time: int = 0
        self._save_data = save_data

    async def open(self) -> "Detector":
        """

        Open the serial port connection. Restarts the detector. clears any
        memory if the detector was previously used.

        :return: self
        :rtype: Detector

        :raises Exception: If the serial port is already open.
        """
        if self._reader is not None:
            raise Exception("port already open")
        reader, writer = await open_serial_connection(url=self.port, baudrate=9600)
        self._reader = reader
        self._writer = writer

        for _ in range(6):
            await reader.readline()

        # 0.9 is the delay time of the detector measurement (time in ms)
        self._start_time = int(time.time() * 1000) + 900
        self._events.clear()

        return self

    async def close(self) -> None:
        """Close the serial port connection."""
        if self._writer is None:
            raise serial.PortNotOpenError

        self._writer.close()
        await self._writer.wait_closed()

        self._reader = None
        self._writer = None

    def run(self, hit_count: int) -> typing.List[HitData]:
        """
        Starts an event loop and gathers the detector data for a specified number of hits.

        :param int hit_count: Number of hits to read from detector.

        :returns: List of all :py:class:`HitData` values gathered.
        """
        events: list = []

        async def run_():
            nonlocal events
            if self.is_open:
                await self.close()
            await self.open()
            for _ in range(hit_count):
                events.append(await self.measurement())
            await self.close()

        asyncio.run(run_())
        return events

    @property
    def is_open(self) -> bool:
        """Check if the detectors is open."""
        return self._reader is not None

    @property
    def start_time(self) -> int:
        """Get the computer time when the detector was last opened in ms."""
        return self._start_time

    async def measurement(self) -> HitData:
        """
        Wait for the detector to register a hit and send the data to the computer.

        Example Usage::
            >>> async def main():
            >>>     detector = await Detector("/dev/ttyUSB0").open()
            >>>     data = await detector.measurement()
            >>>     print(data)

        :return: Data Send through the serial port.
        :rtype: HitData
        """
        if self._reader is None:
            raise serial.PortNotOpenError

        line = await self._reader.readline()
        output = line.decode()
        # data = output.split()

        hit_data = parse_hit_data(output, self._start_time)

        if self._save_data:
            # self._events.append(dct)
            self._events.append(hit_data)
        else:
            self._events = [hit_data]

        return hit_data

    @property
    def rate(self) -> float:
        """

        Get the number of particle detections per second.

        :return: Detection rate.
        :rtype: float
        """
        return (self[0].comp_time - self._start_time) / 1000

    def __iter__(self) -> typing.Iterator[HitData]:
        """Create an iterator over the HitData."""
        return self._events.__iter__()

    async def __aenter__(self):
        if self.is_open:
            await self.close()
        await self.open()
        return self

    async def __aexit__(self, *args):
        await self.close()

    def __getitem__(self, index: int) -> HitData:
        return self._events[index]

    def __len__(self) -> int:
        return len(self._events)
