import obd;
import time

# connection = obd.OBD() #auto connect

# ports = odb.scanSerial()#return list of all USB ports
# print(ports)
# connection = obd.OBD(ports[0])#connect to the first port in the list
# # cmd = obd.commands.RPM
# # response = connection.query(cmd)
# # print(response.value)
# # print(response.unit);



# connection = obd.OBD()

# while connection.is_connected():
#     rpm = connection.query(obd.commands.RPM)
#     speed = connection.query(obd.commands.SPEED)

#     print("RPM:", rpm.value, "| Speed:", speed.value)
#     time.sleep(1)

# connection.close()

ports = obd.scan_serial()  

for port in ports: 
    print ("port: " + port)


connection = obd.OBD("\\.\COM4")  

print("Connection status:", connection.status())

rpm = connection.query(obd.commands.RPM)

print(rpm.value)


