import pywatch.server.main as main
import typing
from pywatch.parse_setup import parse_module


def start_webapp(path: str, host: typing.Optional[str], port: typing.Optional[int]) -> None:
    main.path = path

    main.app.run(host=host, port=port)
