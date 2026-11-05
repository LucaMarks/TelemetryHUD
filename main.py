import odb;

connection = obd.OBD() #auto connect

ports = odb.scanSerial()#return list of all USB ports
print(ports)
connection = obd.OBD(ports[0])#connect to the first port in the list
# cmd = obd.commands.RPM
# response = connection.query(cmd)
# print(response.value)
# print(response.unit);
