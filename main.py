"""Check python-OBD, or read a single RPM/speed sample from an explicit port."""

import argparse
import logging
import math
from pathlib import Path
import subprocess
import sys


def positive_seconds(value):
    seconds = float(value)
    if not math.isfinite(seconds) or seconds <= 0:
        raise argparse.ArgumentTypeError("must be a finite number greater than zero")
    return seconds


def run_check(args):
    print("Importing obd...", flush=True)
    try:
        import obd
    except ImportError as exc:
        print(f"Could not import obd: {exc}", file=sys.stderr, flush=True)
        print('Install it in this environment with: python -m pip install obd',
              file=sys.stderr, flush=True)
        return 1

    print(f"python-OBD {obd.__version__} imported successfully.", flush=True)
    if args.debug:
        obd.logger.setLevel(logging.DEBUG)

    if args.list_ports:
        # Enumerate devices without opening every COM port, as scan_serial does.
        from serial.tools import list_ports

        print("Listing serial devices...", flush=True)
        ports = list(list_ports.comports())
        for port in ports:
            print(f"  {port.device}: {port.description}", flush=True)
        if not ports:
            print("No serial devices found.", flush=True)
        return 0

    if not args.port:
        print("Package check complete; no vehicle connection was attempted.", flush=True)
        print("Use --list-ports to find devices, then --port COM3 to read a vehicle.",
              flush=True)
        return 0

    connection = None
    try:
        print(f"Connecting to {args.port}...", flush=True)
        connection = obd.OBD(portstr=args.port, timeout=1)
        print(f"Connection status: {connection.status()}", flush=True)
        if not connection.is_connected():
            print("No vehicle connection. Check the port, adapter, and vehicle ignition.",
                  flush=True)
            return 1

        print("Reading RPM and speed...", flush=True)
        rpm = connection.query(obd.commands.RPM)
        speed = connection.query(obd.commands.SPEED)
        print("RPM:", rpm.value, "| Speed:", speed.value, flush=True)
        if rpm.is_null() or speed.is_null():
            print("A None value means the vehicle returned no usable data for that command.",
                  flush=True)
        return 0
    finally:
        if connection is not None:
            print("Closing connection...", flush=True)
            connection.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--port", help="OBD adapter port, for example COM3")
    mode.add_argument("--list-ports", action="store_true",
                      help="list serial devices without opening them")
    parser.add_argument("--debug", action="store_true", help="show python-OBD debug logs")
    parser.add_argument("--timeout", type=positive_seconds, default=30,
                        help="maximum total run time in seconds (default: 30)")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    if args.worker:
        return run_check(args)

    print(f"Starting OBD check with {sys.executable}", flush=True)
    # Keep hardware/driver calls out of the supervising process so Ctrl+C and
    # the overall deadline can stop even an unresponsive serial operation.
    command = [sys.executable, "-u", str(Path(__file__).resolve()), "--worker"]
    if args.port:
        command.extend(["--port", args.port])
    if args.list_ports:
        command.append("--list-ports")
    if args.debug:
        command.append("--debug")
    worker = subprocess.Popen(command)
    try:
        return worker.wait(timeout=args.timeout)
    except subprocess.TimeoutExpired:
        print(f"Stopped after {args.timeout:g} seconds. The last message shows where it stalled. "
              "Use --debug for connection details.", file=sys.stderr, flush=True)
        return 1
    except KeyboardInterrupt:
        print("\nStopped by Ctrl+C.", flush=True)
        return 130
    finally:
        if worker.poll() is None:
            worker.kill()
        worker.wait()


if __name__ == "__main__":
    sys.exit(main())
