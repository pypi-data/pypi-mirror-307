from multiprocessing import Pipe
from threading import Thread
import typing


class PoolThread:
    """

    A Class that starts a thread, to which one can add functions to
    be run in that thread. with the ``Thread`` class of the ``threading`` module,
    it is only possible to run a single target function in a thread, but instantiating
    a thread takes time, which can distort the functionality of the ``DetectorPool`` class

    Example:
        >>> def fib(x):
        >>>     if x < 2:
        >>>         return 1
        >>>     return fib(x - 1) + fib(x - 2)
        >>>
        >>> thread = PoolThread()
        >>> thread.start()
        >>>
        >>> thread.pass_function(fib, 45)
        >>> thread.pass_function(fib, 50)
        >>> print("Hello There")
        >>> thread.join()
    The code above creates a thread and calculates the fibonacci numbers for the input 45 and 50
    without blocking the main thread

    """

    def __init__(self):
        # self._thread = Thread(target=self.__worker, args=())
        self._thread: typing.Optional[Thread] = None

        c1, c2 = Pipe()
        self._c1 = c1
        self._c2 = c2

    def start(self) -> None:
        """

        Start the thread.

        """
        self._thread = Thread(target=self.__worker, args=())
        self._thread.start()

    def join(self):
        """

        Just like ``Thread.join()``.

        """
        self._c2.send((None, []))
        self._thread.join()
        self._thread = None

    def __worker(self):
        while True:
            function, args = self._c1.recv()
            if function is not None:
                function(*args)
            else:
                break

    def pass_function(self, function: typing.Callable, *args: typing.Any) -> None:
        """

        Pass a function into the running thread.

        :param type typing.Callable function: A function that should be run inside the thread
        :param args: necessary arguments for the function

        """

        if self._thread is None:
            self.start()
        self._c2.send((function, args))
