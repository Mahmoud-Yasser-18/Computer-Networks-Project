import socket 
from socket import *
import sys
import time
from time import sleep
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

clientPort=int(sys.argv[1])

clientSocket=socket(AF_INET,SOCK_DGRAM)
clientSocket.bind(("",clientPort))
current_package = 0
probability_of_loss= 0.1
result=""
while True :
    print("client waiting")
    msg,addr=clientSocket.recvfrom(2048)
    msg=msg.decode().split('\r\n', 1)
    if int(msg[0])== current_package:
        print("packet 0 recived")
        current_package+=1
        break
    clientSocket.sendto(str(current_package).encode(),addr)

Number_of_segments= int (msg[1])
print("Number of segments ",Number_of_segments)
time0= time.time()
times= [(0,0)]
while current_package<Number_of_segments :
    msg,addr=clientSocket.recvfrom(2048)
    msg=msg.decode().split('\r\n', 1)
    times.append((time.time()-time0,int(msg[0])))
    if int(msg[0])== current_package:
        current_package+=1
        result=result+msg[1]
    
    if np.random.uniform()<probability_of_loss:
        continue

    print("packet" ,current_package,"ACKed" )
    clientSocket.sendto(str(current_package).encode(),addr)
print("Total time = ",times[-1][0]," seconds")
plt.plot(*zip(*times))
plt.title('Recived Packets with time')
plt.xlabel('time')
plt.ylabel('Packet ID')
plt.savefig(f'plot_{times[-1][1]+time0}.png')
f = open(f"result_file_{times[-1][1]+time0}.txt", "a")
f.write(result)
f.close()

# This part of code is to ensure that the sender has recived the last ack packet.

T = 0.2
clientSocket.settimeout(3*T)
while True :
    try:
        msg,addr=clientSocket.recvfrom(2048)
        if np.random.uniform()<probability_of_loss:
            continue
        print("packet" ,current_package,"ACKed" )
        clientSocket.sendto(str(current_package).encode(),addr)
    except:
        break