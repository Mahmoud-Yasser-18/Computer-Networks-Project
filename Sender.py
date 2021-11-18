#Welcoming Socket
import time 
import numpy as np
from socket import *
import sys

reciverPort =int(sys.argv[3])
hostname=sys.argv[2]

clientSocket= socket(AF_INET,SOCK_DGRAM)


MMS = 1300
N_window= 70

T = 0.05
clientSocket.settimeout(T)


current_window_begin=0
current_package=0


filename= sys.argv[1]
## Reading the file : 
with open(filename, 'r') as f:
    file = f.read() 


# Segmenting the file and making the header 
 
Number_of_segments= np.ceil(len(file)/MMS).astype(int)
segments=[f"{i+1}\r\n{file[i*MMS:(i+1)*MMS]}" for i in range(0,Number_of_segments) ] # inserting data segments 
segments.insert(0,f"0\r\n{Number_of_segments+1}") # inserting the first segment
print(segments)
probability_of_loss= 0.1
timeout_list=[]
while True :
    # Taking input
    if (current_package < current_window_begin+N_window) :
        timeout_list=[]
        for i in range (current_package,current_window_begin+N_window+1):
            if np.random.uniform()<probability_of_loss:
                current_package+=1
                continue
            if  (current_package<Number_of_segments+1):
                current_package+=1
                print ("current package",current_package)
                clientSocket.sendto(segments[current_package-1].encode(),(hostname,reciverPort))
                timeout_list.append(time.time())
            else:
                break
            
    
    try:
        if (time.time()<timeout_list[0]+T):
            msg,addr=clientSocket.recvfrom(2048)
            if int(msg.decode())>current_window_begin:
                timeout_list=timeout_list[int(msg.decode())-current_window_begin]
                current_window_begin= int(msg.decode())+1
                print("Packet",msg.decode(), " ACKed")
            if current_window_begin >Number_of_segments:
                print("Message Successfully Sent !")
                break
        raise ValueError(" ")
    except KeyboardInterrupt:
        quit()
    except:
        current_package=current_window_begin-1    