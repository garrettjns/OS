import os
import argparse
from socket import *
import select
import time
import random

parser = argparse.ArgumentParser(description="a chatbot program")

def sorry(inp):
    return "\nSorry, I don't understand " + "\'" + inp + "\'"

def socket_handler():
    # The server is listening at 8080 
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.setblocking(0)
    tcpSerSock.bind(("localhost", 8080))
    tcpSerSock.listen(5)
    return tcpSerSock

# responses

gender = {"female" : "\nHow excellent! Are you a CS major?\n", "male" : "\nMe too. Are you a CS Major?\n"}

cs_major = {"no" : "\nToo bad. Anyway, what's an animal you don't like, and two you do?\n",
            "yes" : "\nExcellent, I am too. What's an animal you don't like, and two you do?\n"}

def response1(inp):
    if "female" in inp.lower() or "woman" in inp.lower():
        return(gender["female"])
    elif "male" in inp.lower() or "man" in inp.lower():
        return(gender["male"])
    elif "bye" in inp.lower():
        return 0
    else:
        return(sorry(inp) + "\nAnyway, are you a CS major?\n")

def response2(inp):
    if "no" in inp.lower() or "nah" in inp.lower():
        return(cs_major["no"])
    elif "yes" in inp.lower() or "yea" in inp.lower():
        return(cs_major["yes"])
    elif "bye" in inp.lower():
        return 0
    else:
        return(sorry(inp) + "\nAnyway, what's an animal you don't like, and two you do?\n")

def response3(inp):
    if "," in inp:
        inp = inp.split(",")
    elif "and" in inp:
        inp = inp.split("and")
    elif "bye" in inp.lower():
        return 0
    else:
        inp = inp.split(" ")
    if len(inp) < 2:
        return 0
    return("\n\n" + inp[1] + " are awesome, but I hate " + inp[0] + " too.")

socket_states = {}

server_sock = socket_handler()

inputs = [server_sock]

def delete_socket(s):
    s.send(b'Goodbye for now!')
    del socket_states[s]
    inputs.remove(s)
    s.close()

#introduces delay before send
def time_func():
    print(time.sleep(int(4*random.random())))
    
while inputs:
    readable, _, exceptional = select.select(inputs, inputs, inputs)

    for s in readable:
        if s is server_sock:
            
            # A "readable" server socket is ready to accept a connection
            client_sock, addr = s.accept()
            print('Received a connection from:', addr)
            client_sock.setblocking(0)
            inputs.append(client_sock)
            socket_states[client_sock] = 1
            client_sock.send(b'\nHello, are you male or female?\n')
        else:
            print(s.getpeername(), ": ", socket_states[s])
            data = s.recv(4096)
            if data:
                # A readable client socket has data
                if socket_states[s] == 1:
                    response = response1(data.decode())
                    if response == 0:
                        delete_socket(s)
                        continue
                    time_func()
                    s.send(response.encode())
                    socket_states[s] = 2
                    
                elif socket_states[s] == 2:
                    response = response2(data.decode())
                    if response == 0:
                        delete_socket(s)
                        continue
                    time_func()
                    s.send(response.encode())
                    socket_states[s] = 3
                
                elif socket_states[s] == 3:
                    response = response3(data.decode())
                    if response == 0:
                        delete_socket(s)
                        continue
                    time_func()
                    s.send(response.encode() + b'\nGoodbye for now!')
                    del socket_states[s]
                    inputs.remove(s)
                    s.close()
                
    for s in exceptional:
        print ('handling exceptional condition for', s.getpeername())
        # Stop listening for input on the connection
        delete_socket(s)
