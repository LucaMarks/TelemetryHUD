import obd;
import time;
import os;

# connection = obd.OBD() #auto connect

# ports = odb.scanSerial()#return list of all USB ports
# print(ports)
# connection = obd.OBD(ports[0])#connect to the first port in the list
# # cmd = obd.commands.RPM
# # response = connection.query(cmd)
# # print(response.value)
# # print(response.unit);
#lucas code


# connection = obd.OBD()

# while connection.is_connected():
#     rpm = connection.query(obd.commands.RPM)
#     speed = connection.query(obd.commands.SPEED)

#     print("RPM:", rpm.value, "| Speed:", speed.value)
#     time.sleep(1)

# connection.close()

# ports = obd.scan_serial()  

# for port in ports: 
#     print ("port: " + port)


# connection = obd.OBD("\\.\COM5")  

# print("Connection status:", connection.status())

# rpm = connection.query(obd.commands.RPM)

# print(rpm.value)
#my code




# import serial
# import time

# connection = serial.Serial("COM5", 38400, timeout=10)

# def send_command(command):
#     connection.reset_input_buffer()
#     connection.write((command + "\r").encode())

#     response = connection.read_until(b">")

#     print(f"{command}: {response.decode(errors='replace').strip()}")
#     print()

# try:
#     time.sleep(2)

#     send_command("ATZ")     # Reset adapter
#     send_command("ATE0")    # Disable echo
#     send_command("ATL0")    # Disable linefeeds
#     send_command("ATSP6")   # Select CAN 11-bit, 500 kbps

#     send_command("0100")    # Request supported PIDs
#     send_command("010C")    # Request engine RPM
#     send_command("010D")    # Request vehicle speed

# finally:
#     connection.close()

import obd

ports = obd.scan_serial()

for port in ports:
    print("Port:", port)

# Connect to the OBD-II adapter
connection = obd.OBD(
    portstr="COM5",
    baudrate=38400,
    protocol="6",
    fast=False,
    timeout=5
)

print("Connection status:", connection.status())
while True:
    # Read engine RPM
    rpm = connection.query(obd.commands.RPM)
    speed = connection.query(obd.commands.SPEED)
    

    if not rpm.is_null():
        os.system("cls")
        print("Engine RPM:", rpm.value.magnitude, "| Speed:", speed.value.magnitude,)
    else:
        print("RPM data unavailable")

connection.close()