import socket
import time
import threading
global report
report = []

def Scan(port):
    cache_res = ''
    ip = '10.0.2.5'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    result = s.connect_ex((ip, port))
    
    if result == 0:
        cache_res = '{} port is open!'.format(port)
        report.append(cache_res)
    s.close()

start_time = time.time()

'''
for x in range(19, 25):
    Scan(x)
'''

threads = [threading.Thread(target=Scan, args = (n,)) for n in range(1,65536)]
[t.start() for t in threads]
[t.join() for t in threads]

print(report)
print("--------%.2fs Seconds ----------" %(time.time() - start_time))

