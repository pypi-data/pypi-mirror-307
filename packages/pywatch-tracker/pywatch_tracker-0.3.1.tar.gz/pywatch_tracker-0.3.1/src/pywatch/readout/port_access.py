import pathlib
import time
import typing

import serial
import serial.tools.list_ports as lp
from serial import Serial


def get_serial_ports() -> typing.List[Serial]:
    """

    List all available serial ports on the system. Should work on all
    plattforms.
    on Linux: To read be able to read and write to serial ports,
    you need either admin privileges or be part of the dialout group.

    :return: list of all connected serial ports.
    :rtype: list[Serial]

    """

    ports = lp.comports()

    serial_ports = []

    for p in ports:
        try:
            sp = Serial(p.device)
            serial_ports.append(sp)
        except ValueError as e:
            print(p.device, e)
        except serial.SerialException as _:
            pass
        except:
            print("unknown exception when looking for serial ports")

    return serial_ports


def print_ports(ports: typing.List[Serial]):
    """Enumerate all available ports and print to the console"""
    for i, port in enumerate(ports):
        print(f"[{i + 1}] {port.port}")


def input_index_from_user_for_port(port: Serial) -> int:
    """

    Open a serial port and ask the user to enter an index.

    If the serial port is a CosmicWatch Detector, the detector will restart
    and the user will be able to see that.

    :param Serial port: serial port

    :return: Number the user selected
    :rtype: int

    """
    print(f"Opening port {port.port}")
    if port.is_open:
        port.close()
    port.open()
    index = int(input("Enter index: "))
    port.close()

    return index


def input_sorted_port_list(ports: typing.List[Serial]) -> typing.List[Serial]:
    """

    User sorts the Serial port list to its liking.

    :param Serial ports: list of connected serial ports
    :return: sorted list of serial ports
    :rtype: list[Serial]

    """
    indices = []
    i = 0
    while i < len(ports):
        if i < len(indices):
            del indices[i]
        print(indices)
        port = ports[i]
        print(f"Opening port {port.port}")

        if port.is_open:
            port.close()
        port.open()
        while True:
            try:
                index = input("Enter index: ")
                if index.lower() in ["back", "return"]:
                    break
                index = int(index)
                if index >= 0 and index in indices:
                    raise ValueError("Index already in list")
                break
            except ValueError as e:
                print(str(e))
        if isinstance(index, int):
            indices.append(index)
            i += 1
        else:
            if i == 0:
                print("Cannot go to previous port because this is the first one.")
            else:
                i -= 1

    ports_sorted = sorted([(index, port) for index, port in zip(indices, ports)], key=lambda x: x[0])
    indices = [x[0] for x in ports_sorted if x[0] >= 0]
    if max(indices) != len(indices) - 1:
        print("Warning: the indices do not match the number of ports.")
        yesno = input("Do you want to restart? (yes/no): ")
        if yesno.lower() in ["yes", "y"]:
            return input_sorted_port_list(ports)
    ports_sorted = [x[1] for x in ports_sorted if x[0] >= 0]

    return ports_sorted


def input_ports_from_commandline():
    """Command line interface for sorting ports and saving in a file."""
    old_ports = get_serial_ports()

    text = """
    You will now see the ports restarting simultaneously.
    After that each one of them will restart separately and you will be prompted to input the order
    of the detectors beginning from 0. If you don't see the detector blinking, it means that this serial port 
    is not a detector. If you don't want a serial port in the list, give that port a negative index.
    If you miss an Index you will be prompted to decide 
    to either restart the numbering or leave as is. 
    You can go back to the previous detector by typing 'back' or 'return' if you gave a detector 
    the wrong index.  
    """
    print(text)

    input("press Enter to start: ")

    while True:
        ports = input_sorted_port_list(old_ports)
        if yesno("Do you want to test the ports? (yes/no): "):
            test_ports(ports)
            if yesno("Do you want to restart? (yes/no): "):
                continue
        break

    save_str = "PORTS = [\n"
    for port in ports:
        save_str += f"    '{port.port}',\n"
    save_str += "]\n"

    while True:
        file_path = input("Where to save the ports?: ")
        path = pathlib.Path(file_path)
        if not path.parent.exists():
            print("Directory does not exist")
            continue
        if path.exists():
            if not yesno("The File already exists. Do you want to overwrite it? (yes/no): "):
                continue
        try:
            with open(file_path, "w") as f:
                f.write(save_str)
            break
        except IOError as e:
            print(str(e))

    print("Ports saved")


def user_input_serial_port() -> Serial:
    """let the user choose one of the available serial ports"""
    ports: typing.List[Serial] = get_serial_ports()
    if len(ports) == 0:
        text = "no port was found. Check if you have permission to access the port"
        raise Exception(text)

    print("Choose one of the following ports:\n")
    print_ports(ports)
    while True:
        try:
            i = int(input(""))
        except ValueError:
            print("you have to enter an index")
            continue

        if i < 1 or i > len(ports):
            print("invalid index")
            continue

        return ports[i - 1]


def test_ports(ports: typing.List[Serial]) -> None:
    """Test the ports by opening them one after the other."""
    for index, port in enumerate(ports):
        print(f"{port.name} with index {index}")
        if port.is_open:
            port.close()
        port.open()
        time.sleep(2)


def yesno(text: str) -> bool:
    """Interface for asking the user a yes/no question"""
    yesno_ = input(text)
    while True:
        if yesno_.lower() in ["yes", "y"]:
            return True
        elif yesno_.lower() in ["no", "n"]:
            return False
        else:
            print("invalid input")
