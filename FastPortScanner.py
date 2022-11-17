import socket
import time
import threading
import sys
from termcolor import colored, cprint
import colorama
import os

colorama.init()

from BannerReading import Grabber

global report
report = []

os.system('color A')

def Scan(ip, Fport, Lport, port):
    cache_res = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((ip, port))
    
    if result == 0:
        cache_res = port
        report.append(int(cache_res))
        cprint(".",'red','on_grey',end='') # design
    s.close()

def Start_Scan():
    cprint("Enter the ip address of the machine you want to scan: ", "blue", "on_grey",attrs=["bold"],end='')
    ip = input()
    cprint("Enter the port from which you want to start scan from: ", "blue", "on_grey",attrs=["bold"] ,end='')
    Fport = int(input())
    cprint("Enter the last port you want to scan till: ", "blue", "on_grey",attrs=["bold"] ,end='') # on grey - provides same background color so, it doesn't looks like if it's been overwritten.
    Lport = int(input())
    cprint("\nScanning please wait.",'cyan','on_grey',attrs=["dark"],end='')
    
# Time the scanner
    start_time = time.time()
    
    threads = [threading.Thread(target=Scan, args = (ip,Fport, Lport, n)) for n in range(Fport,Lport+1)]
    [t.start() for t in threads]
    [t.join() for t in threads]

    cprint("\n\nOpen ports are: ",'yellow','on_grey',attrs=["bold"])
    counter = 0
    
    for x in report:
        cprint('                 > ', 'green', 'on_grey', attrs=['bold'], end='')
        cprint('Port No. ','blue','on_grey',attrs=['bold'],end='')
        cprint(x,'red','on_grey',attrs=["bold"])
    cprint("\nScanned in -------- %.2fs Seconds ----------\n\n" %(time.time() - start_time),'green','on_grey',attrs=["bold"])
    
    
    time.sleep(100000)


def Design():
    print("""
    ______        _  ______          _   _____                                 
    |  ___|      | | | ___ \        | | /  ___|                                
    | |_ __ _ ___| |_| |_/ /__  _ __| |_\ `--.  ___ __ _ _ __  _ __   ___ _ __ 
    |  _/ _` / __| __|  __/ _ \| '__| __|`--. \/ __/ _` | '_ \| '_ \ / _ \ '__|
    | || (_| \__ \ |_| | | (_) | |  | |_/\__/ / (_| (_| | | | | | | |  __/ |   
    \_| \__,_|___/\__\_|  \___/|_|   \__\____/ \___\__,_|_| |_|_| |_|\___|_|                                                                          
                                                            v1.0 by Stefen                                                              
    """)


Design()
Start_Scan()
