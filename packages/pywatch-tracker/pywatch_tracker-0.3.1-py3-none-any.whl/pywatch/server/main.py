import asyncio
import pathlib
import typing
import traceback
from types import ModuleType

from quart import Quart, render_template, websocket
from werkzeug.utils import send_from_directory

from pywatch.parse_setup import parse_module
from .color import *
from .detector_logic_calculation import *
from .simulation import SimulationPool
from ..readout import DetectorPool, EventData, PoolThread


SRC_DIR = pathlib.Path(__file__).parent.parent.parent.resolve()
"""source directory of the python package"""

setup_mod: typing.Optional[ModuleType] = None
path: typing.Optional[str] = None
app = Quart(__name__, template_folder="../dist/", static_folder="../dist/assets")

detectors = []
color = ColorRange(10, 80, Color("blue"), Color("red"))


async def show_msg(msg: str, error: bool = False, trace: typing.Optional[str] = None):
    await websocket.send_json({
        "type" : "msg",
        "error": error,
        "msg"  : msg,
        "trace": trace if trace else "",
    })


@app.route("/")
async def main():
    global setup_mod

    if path is None:
        raise RuntimeError("Setup Script was not set")
    module_ = parse_module("Setup_Module", path)
    setup_mod = module_

    return await render_template("index.html")


@app.route("/<file_name>")
async def serve_file(file_name):
    print(SRC_DIR / "pywatch/dist/assets")
    return send_from_directory(SRC_DIR / "pywatch/dist/assets", file_name, environ={"REQUEST_METHOD": "GET"})


@app.websocket("/measurement")
async def ws():
    if setup_mod.EVENT_COUNT is not None:
        await websocket.send_json({
            "type" : "event_count",
            "count": setup_mod.EVENT_COUNT,
        })
    while True:
        data = (await websocket.receive_json())["data"]
        if data["type"] == "start":
            print("start measurement")
            await websocket.send_json({
                "type": "start",
            })
            await show_msg("Starting Measurement")
            event_count = data["eventCount"]

            async def callback(event: EventData, thread: PoolThread):
                voltage = sum([hit_data.sipm_voltage for hit_data in event.values()]) / len(event)
                print(color(voltage))
                msg: dict = {
                    "type" : "event",
                    "data" : event.to_dict(),
                    "color": color(voltage),
                }

                await websocket.send_json(msg)

            if len(detectors) is None:
                print("No Detector geometry was given. Try Again")
                continue
            try:
                if setup_mod.SIMULATION:
                    print("len", len(detectors))
                    pool = SimulationPool(detectors, 1, 0.1)
                    await pool.async_run(event_count, callback)
                else:
                    pool = DetectorPool(*setup_mod.PORTS, threshold=setup_mod.THRESHOLD)
                    await pool.async_run(event_count, callback, callback_solo_hits=True)
            except Exception as e:
                await show_msg(str(e), True, traceback.format_exc())
            else:
                await show_msg("Measurement Finished")
            finally:
                await websocket.send_json({
                    "type": "stop",
                })


@app.websocket("/logic")
async def ws_logic():
    global detectors

    if setup_mod.GEOMETRY_FILE is not None:
        with open(setup_mod.GEOMETRY_FILE, "r") as f:
            file_output = f.read()
        data = await websocket.receive_json()
        if data["type"] != "load":
            raise Exception("Wrong Message Type Received")
        await websocket.send_json({
            "type": "detectors",
            "file": file_output,
        })
        try:
            await show_msg("Calculating Logic...", False)
            detectors, coin = load_from_json(setup_mod.SEGMENTATION, setup_mod.GEOMETRY_FILE)
            await websocket.send_json(coin.to_dict("mean"))
            print("logic send")
            await show_msg("Logic Calculated Successfully", False)
        except:
            await show_msg("Could Not Load Coincidences. Error In Geometry File", True)

    while True:
        data = await websocket.receive_json()
        if data["type"] != "geometry":
            continue
        data = data["detectors"]
        detectors.clear()
        # TODO load rotation
        for d in data:
            position = Vector(*d["position"].values())
            rot_values = [0, 0, 0, "XYZ"]
            v = d.get("rotation")
            if v is not None:
                rot_values = list(v.values())[1:]

            detectors.append(Detector(setup_mod.SEGMENTATION, position, (rot_values[-1], Vector(*rot_values[:-1]))))

        coin = calculate_coincidences(detectors)
        await websocket.send_json(coin.to_dict("mean"))
        print("logic send")
        await show_msg("Logic Calculated Successfully", False)

    # pprint(detectors)
