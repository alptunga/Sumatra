import wmi
import re

SERVERS=[]
SERVICES=[]

def wmi_connection(server, username, password):
    print "\nattempting connection with", server
    return wmi.WMI(server, user=username, password=password)

def servicecheck(connection):

    for services in SERVICES:
       for service in connection.Win32_Service(name=services):
           if service.State == 'Running':
               print server, service.Caption, service.State
           else: 
               if service.State==('Stopped' or "Start Pending" or "Stop Pending" or "Continue Pending" or "Paused" or "Unknown" ):
                 print server, service.Caption, service.State, "Attempting to start service."
                 StartServiceStatus=service.StartService()
                 if StartServiceStatus == "0":
                   print "Service is Starting."
                 else:
                   print "Service is NOT Starting."
    return
       
           
def diskcheck(connection):
    for disk in connection.Win32_LogicalDisk (DriveType=3):
        if disk.Caption=="C:":
           print disk.Caption, "%0.2f%% free" % (100.0 * long (disk.FreeSpace) / long (disk.Size)) 
           return
def oscheck(connection):
     for os in connection.Win32_OperatingSystem():
         print os.Caption,"\n"
         return

def checkall(server, username, password):
    connection = wmi_connection(server, username, password)
    oscheck(connection)
    diskcheck(connection)                            
    servicecheck(connection)
    return

file = open("SERVERS.txt","r")


for line in file:
    line = line.rstrip()
    SERVERS.append(re.split(',',line))
file.close()

file = open ("SERVICES.txt","r")
for line in file:
    line = line.rstrip()
    print line
    SERVICES.append(line)
print SERVICES
file.close()



for server, username, password in SERVERS:
    checkall(server,username,password)





























