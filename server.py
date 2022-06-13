import socket
import sys

# COMMAND AND CONTROL CODE WILL GO HERE

slaves = list()

with open("slaves.txt", "r") as file:
    content = file.read()
    if(len(content.replace("\n", "")) > 0):
        slaves = content.split("\n")
        slaves = slaves[:-1]

print(slaves)

port = 1234
ip = '127.0.0.1'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('127.0.0.1', port))
    print(f"Bound to {ip}:{str(port)}")
    
    s.listen()
    s.settimeout(5)
    print("Listening")
    try:
        while True:
            try:
                sres, addr = s.accept()
                print(f'Got connection from {addr}')
                sres.sendall(b"Jo dankjewel voor je berichtje")
                sres.close()
                if slaves.count(addr) == 0:
                    slaves.append(addr)
                    with open('slaves.txt', 'w') as file:
                        file.write(f"{addr}\n")
            except KeyboardInterrupt:
                pass
    except KeyboardInterrupt:
        pass