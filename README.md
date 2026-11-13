# TelemetryHUD

Run these commands from this repository's directory with your virtual environment
activated. The Python package is named `obd` (python-OBD).

```powershell
python -m pip install obd
python -u main.py
```

The default run prints the Python executable and python-OBD version, then exits.
It checks the installation without needing an adapter or vehicle and does not
generate simulated telemetry.

To read real vehicle data, connect an OBD-II adapter, turn on the vehicle ignition,
and choose the adapter's actual serial port:

```powershell
python -u main.py --list-ports
python -u main.py --port COM3 --debug
```

Replace `COM3` with your adapter's port. A live run reports the connection status,
reads one RPM/speed sample, closes the connection, and exits. `None` means no usable
value was returned for that command. Listing ports does not open them.

All modes have a 30-second overall limit, including package import and connection
cleanup. Change it with `--timeout 60` if necessary. Ctrl+C stops the run. Hardware
operations run in a child process so the parent can terminate a stalled operation.

The original script attempted an automatic connection before its first print.
On Windows, the installed python-OBD scanner tries opening up to 256 COM ports,
which can stall on a serial/Bluetooth driver. The script also had an
`odb.scanSerial()` typo (the library API is `obd.scan_serial()`) and opened three
connections. Using one explicit port avoids that automatic scan.
