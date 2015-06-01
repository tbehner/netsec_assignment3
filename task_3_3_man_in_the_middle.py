import telnetlib
from time import sleep

def receiveMessage(tn):
    message = tn.read_until("\n", 0.1)
    return message

def sendMessage(tn, message):
    tn.write(message)
    
def printMessage(num, message):
    print "##################################################"
    print num
    print message
    print "##################################################"
    
    
HOST_1 = "10.0.0.12"
PORT_1 = 3333
HOST_2 = "10.0.0.12"
PORT_2 = 4444

tn_1 = telnetlib.Telnet(HOST_1, PORT_1)
tn_2 = telnetlib.Telnet(HOST_2, PORT_2)


while 1==1:
    message = receiveMessage(tn_1)
    if message != "":
        printMessage(1, message)
        sendMessage(tn_2, message)
    sleep(0.05)
    
    message = receiveMessage(tn_2)
    if message != "":
        printMessage(2, message)
        sendMessage(tn_1, message)
    sleep(0.05)