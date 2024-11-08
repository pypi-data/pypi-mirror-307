import asyncio
from copy import deepcopy
from typing import Any, Callable, List, Optional, Union, Tuple

import serial

from .detector import Detector
from .event_data_collection import EventData, EventDataCollection
from .pool_thread import PoolThread


Callback = Union[Callable[[EventData, PoolThread, Any], Any], Callable[[EventData, PoolThread], Any]]
"""Type of callback function for DetectorPool.run() function"""


class DetectorPool:
    """

    Pool of multiple Detectors, which saves coincidence events if multiple hits are registered in
    the threshold time.

    Example Usage
        >>> def callback(event, thread):
        >>>     print(event)
        >>>
        >>> detector_pool = DetectorPool('COM3', 'COM4', callback=callback)
        >>> result = detector_pool.run(100)
        >>> print(result)

    This code measures 100 events and prints the event data after every event.
    It is possible to include complex calculations to the callback function, but
    the measurement needs accurate timings of the computertime when a hit occurs,
    which cannot be given if the callback function blocks the reading of the serial ports.
    Blocking tasks should be run in another thread as follows:
        >>> # Fibonacci sequence. Takes a lot of time to calculate
        >>> def fib(n):
        >>>    if n < 2:
        >>>         return n
        >>>    return fib(n - 1) + fib(n - 2)
        >>>
        >>> def callback(event, thread):
        >>>     thread.pass_function(fib, 45)
        >>>     print(event)
        >>>
        >>> detector_pool = DetectorPool('COM3', 'COM4', callback=callback)
        >>> result = detector_pool.run(100)
        >>> print(result)

    The ``callback`` function can also be an ``async`` function.
        >>> import asyncio
        >>> async def callback(event, thread):
        >>>     await asyncio.sleep(0)
        >>>     print(event)
        >>>
        >>> detector_pool = DetectorPool('COM3', 'COM4', callback=callback)
        >>> result = detector_pool.run(100)
        >>> print(result)

    :param str ports:  Positional Arguments with names of serial ports.
    :param int threshold: Time delta of hits in one coincidence event in ms.

    """

    def __init__(self, *ports: str, threshold: int = 10) -> None:
        self.threshold = threshold
        self._detectors = [Detector(port, False) for port in ports]

        self._thread = PoolThread()

        self._event_data: EventData = EventData()  # make this obsolete

        # stores all the events
        self._data = EventDataCollection()

        self._first_coincidence_hit_time = 0
        self._result: Tuple[int, Optional[Exception]] = (0, None)

    @property
    def result(self) -> Tuple[int, Optional[Exception]]:
        """
        Result of the last measurement.

        :return: Event Count and optional Exception to measurement.
        :rtype: Tuple[int, Optional[Exception]]

        """
        return self._result

    async def open(self) -> "DetectorPool":
        """

        Opens all ports for data collection

        :return: Self.
        :rtype: DetectorPool

        """
        self._data.clear()
        self._first_coincidence_hit_time = 0
        await asyncio.gather(*[port.open() for port in self._detectors])

        return self

    async def close(self) -> None:
        await asyncio.gather(*[port.close() for port in self._detectors])

    @property
    def is_open(self) -> bool:
        return self._detectors[0].is_open

    @property
    def detector_count(self):
        return len(self._detectors)

    @property
    def get_ports(self) -> List[str]:
        """

        Get a list of ports from the used detectors. The index at which a port
        is returned corresponds to the index in the event list.

        """
        return [dt.port for dt in self._detectors]

    @property
    def data(self) -> EventDataCollection:
        """
        :return: Data that was gathered during last measurement.
        :rtype: EventDataCollection
        """
        return self._data

    def run(self,
            event_count: int,
            callback: Optional[Callback] = None,
            *args,
            save_solo_hits: bool = False,
            callback_solo_hits: bool = False
            ) -> (int, Optional[Exception]):
        """
        Make a measurement for coincidence events.

        Example Usage
            >>> def callback(event, thread):
            >>>     print(event)
            >>>
            >>> detector_pool = DetectorPool('COM3', 'COM4', callback=callback)
            >>> result = detector_pool.run(100)
            >>> print(result)

        :param int event_count: Number of events that need to be registered
        :param Optional[Callback] callback: Callback function that is executed after every event. Can be an async
        function
        :param args: optional positional arguments of ``callback``
        :param type bool save_solo_hits: Save hits, that are not coincidences, in the data
        :param type bool callback_solo_hits: forward hit data as event data, event if not a coincidence

        :return: Number of measured events and exception that was raised during measurement if any.
        :rtype: Tuple[int, Optional[Exception]]
        """
        # keine Ahnung, ob das so gut ist
        try:
            asyncio.get_running_loop().run_until_complete(self.async_run(event_count, callback, *args))
        except RuntimeError:
            asyncio.run(self.async_run(event_count, callback, *args))

        return self._result

    async def async_run(self, event_count: int, callback: Optional[Callback] = None, *args,
                        save_solo_hits: bool = False, callback_solo_hits: bool = False
                        ) -> (int, Optional[Exception]):
        await self.open()
        await self.close()
        await self.open()
        if callback is not None:
            self._thread.start()
        finished = False
        counted_hits = 0  # bad name, because it counts coincidences
        lock = asyncio.Lock()

        async def run_detector(dt: Detector, dt_index: int) -> (int, Optional[Exception]):
            """reads hits asynchronously for the specified detector. if the hit time is not inside
            the threshold anymore, save the current event and begin a new one with the current hit time
            as first coincidence time."""
            nonlocal finished, counted_hits, lock
            exc = None

            while not finished:
                try:
                    await dt.measurement()
                except (asyncio.CancelledError, Exception, serial.SerialException) as e:
                    print(f"{e}")
                    finished = True
                    exc = e
                    break

                if dt[-1].comp_time - self._first_coincidence_hit_time <= self.threshold:
                    if dt_index in self._event_data.keys():
                        continue
                    self._event_data[dt_index] = dt[-1]
                else:
                    # print(self._event)
                    if len(self._event_data.keys()) > 1 or save_solo_hits:
                        self._data.add_event(deepcopy(self._event_data))
                    if len(self._event_data.keys()) > 1 or (callback_solo_hits and len(self._event_data.keys()) > 0):
                        if callback is not None:
                            coro = callback(self._event_data, self._thread, *args)
                            if asyncio.iscoroutinefunction(callback):
                                await coro

                    if len(self._event_data.keys()) > 1:
                        async with lock:
                            counted_hits += 1

                        # print(f"hit {counted_hits} / {hits}")
                    if counted_hits == event_count:
                        finished = True
                        break

                    self._first_coincidence_hit_time = dt[-1].comp_time
                    self._event_data.clear()
                    self._event_data[dt_index] = dt[-1]

            return counted_hits, exc

        async def measure_task() -> (int, Optional[Exception]):
            tasks = [
                asyncio.create_task(
                    run_detector(self._detectors[i], i)  # , name=self._detectors[i].port
                )
                for i in range(len(self._detectors))
            ]
            completed, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

            for task in pending:
                task.cancel()

            return completed.pop().result()

        result = await measure_task()

        if callback is not None:
            self._thread.join()
        await self.close()

        self._result = result
        return result

    def __len__(self) -> int:
        return len(self._data)

    async def __aenter__(self):
        if self.is_open:
            await self.close()
        await self.open()

        return self

    async def __aexit__(self, type_, value, traceback):
        await self.close()
