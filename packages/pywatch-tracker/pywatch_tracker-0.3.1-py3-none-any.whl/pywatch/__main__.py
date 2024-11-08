import argparse
import pathlib
from .readout.measurement import measurement_from_script
from .readout.port_access import input_ports_from_commandline
from .server import start_webapp


parser = argparse.ArgumentParser(
    prog="pywatch",
    description="""WebApp for a 3D Tracker
    with CosmicWatch scintillation Detectors"""
)
parser.add_argument("subcommand",
                    choices=[
                        "measurement",
                        "webapp",
                        "set-ports",
                        "help"
                    ])
parser.add_argument("path", nargs="?", type=pathlib.Path)
parser.add_argument("--host", help="host to bind webapp to")
parser.add_argument("--port", help="port to bind webapp to")
args = parser.parse_args()
if args.subcommand == "measurement":
    if args.path is None:
        raise ValueError("Path argument is required")
    measurement_from_script(args.path)
elif args.subcommand == "webapp":
    if args.path is None:
        raise ValueError("Path argument is required")
    start_webapp(args.path, args.host, args.port)
elif args.subcommand == "set-ports":
    input_ports_from_commandline()
elif args.subcommand == "help":
    parser.print_help()
