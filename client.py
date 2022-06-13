import socket
import sys
import selectors
import types

# CODE THAT RUNS ON INFECTED MACHINE WILL GO HERE

HOST = "127.0.0.1"
PORT = 1234

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world")
    data = s.recv(1024)

print(f"Received {data!r}")