from socket import *
import struct, time,traceback,binascii

HOST = "202.204.105.195"
PORT = 3335
BUFSIZ = 128
ADDR=(HOST,PORT)
uid=24670292149586
#1e04000070160000

hexuid=hex(uid)[2:]

hexuid='0000'+hexuid
l=len(hexuid)
data=''
while (l>0):
    s=hexuid[l-8:l]
    l=l-8
    data+=s+'.'
data=data.split('.')
data.pop()
#print(data)
str=struct.pack("ii",int(data[0],16),int(data[1],16))
#print(str)
str2=struct.pack("14i",int(data[0],16),int(data[1],16),
                 int('0000',16),int('0000',16),int('0000',16),int('0000',16),
                 int('0000',16),int('0000',16),int('0000',16),int('0000',16),
                 int('0000',16),int('0000',16),int('0000',16),int('0000',16))

udpsend = socket(AF_INET, SOCK_DGRAM)

while True: 
    udpsend.sendto(str2, ADDR)
    udpsend.settimeout(5)
    try:
        data, ADDR = udpsend.recvfrom(BUFSIZ)
        print (data)
    except error:
        print('Recv time out!')
    if not data:
        print('get Null!')
        break
    time.sleep(60)
    
udpsend.close()