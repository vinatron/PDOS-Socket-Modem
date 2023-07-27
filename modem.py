#!/usr/bin/env python3
import socket
import time
from contextlib import suppress

def do_nothing():
    pass

PDOS = '10.0.0.1'
ICC = '10.0.0.2'
CPORT = 3270
SPORT = 3270

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((PDOS, CPORT))


server.listen(0)
pdos_socket, address = server.accept()
print(f"Connected to {address}")
client.connect((ICC, SPORT))

#time.sleep(1)
#client.send(b'\xff\xfc\x28')
#with suppress(TimeoutError):
idata = client.recv(1024)
print(f'Data from ICC is: {idata}')
idatlen = len(idata)
    #print(f'{idatlen}')
print(f'Data Length from ICC is {idatlen}')
pdos_socket.send(idata)
while True:
    #pdata = pdos_socket.recv(1024)
    #print(f"Data from PDOS is: {pdata}")
    #pdatlen = len(pdata)
    #print(f'{pdatlen}')
    rxbuff = bytearray(b'')
    running = True
    msec = 2
    end = 0
    while running:
        print(msec)
        msec -= 1
        pdos_socket.settimeout(0.5)
        print("before")
        try:
            data = pdos_socket.recv(1)
        except:
            #data = b''
            print("got exception")
        print("after")
        lendata = len(data)
        lenbuf = len(rxbuff)
        print(f'Input Data: {data}' + f' Length: {lendata}' + f'T ime: {msec} Milisecond' + f' Timer Running: {running}')
        print(f'Data in Buffer: {rxbuff}')
        if lendata == None:
            continue
        else:
            rxbuff.extend(data)
            pdata = rxbuff
            print(f"ACCUMULATED Data from PDOS is: {pdata}")
        if msec <= end:
            running = False
            print(f'RX Buffer Full Data: {rxbuff}')
        pdata = rxbuff
        print(f"Data from PDOS is: {pdata}")
        pdatlen = len(pdata)
        print(f'Data Lenght from PDOS is {pdatlen}')
        client.send(pdata)
    #if pdatlen == None:
    #    print('Len Null')
    #    continue
    #else:
    #    print(f'Data Lenght from PDOS is {pdatlen}')
    #    client.send(pdata)
