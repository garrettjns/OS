import argparse
from socket import *
import time
import random
import threading

parser = argparse.ArgumentParser(description="a chatbot program")

# responses

gender = {"female" : "\nHow excellent! Are you a CS major?\n", "male" : "\nMe too. Are you a CS Major?\n"}

cs_major = {"no" : "\nToo bad. Anyway, what's an animal you don't like, and two you do?\n",
            "yes" : "\nExcellent, I am too. What's an animal you don't like, and two you do?\n"}

def sorry(inp):
    return "\nSorry, I don't understand " + "\'" + inp + "\'"

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

def socket_handler():
    # The server is listening at 8080 
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.setblocking(0)
    tcpSerSock.bind(("localhost", 8080))
    tcpSerSock.listen(5)
    return tcpSerSock

def delete_socket(s):
    s.send(b'Goodbye for now!')
    del socket_states[s]
    s.close()

# Introduces delay before send
def time_func():
    print(time.sleep(int(4*random.random())))

def thread_function(client_sock, thread_num):
    print("Thread %d: starting" % (thread_num))
    client_sock.send(b'\nHello, are you male or female?\n')    
    while True:
        try:
            data = client_sock.recv(4096)
        except:
            continue
        if data:
            print(client_sock.getpeername(), ": ", socket_states[client_sock])
            # A readable client socket has data
            if socket_states[client_sock] == 1:
                response = response1(data.decode())
                if response == 0:
                    delete_socket(client_sock)
                    break
                time_func()
                client_sock.send(response.encode())
                socket_states[client_sock] = 2
                
            elif socket_states[client_sock] == 2:
                response = response2(data.decode())
                if response == 0:
                    delete_socket(client_sock)
                    break
                time_func()
                client_sock.send(response.encode())
                socket_states[client_sock] = 3
            
            elif socket_states[client_sock] == 3:
                response = response3(data.decode())
                if response == 0:
                    delete_socket(client_sock)
                    break
                time_func()
                client_sock.send(response.encode() + b'\nGoodbye for now!')
                del socket_states[client_sock]               
                client_sock.close()
                break
    print("Thread %d: finishing" % (thread_num))

server_sock = socket_handler()
thread_num = 0

while True:
    try:
        client_sock, addr = server_sock.accept()
    except:
        continue
    client_sock.setblocking(0)
    socket_states[client_sock] = 1
    thread_num += 1
    print("Main    : create and start thread %d." % (thread_num))
    new_thread = threading.Thread(target=thread_function, args=(client_sock, thread_num,))
    new_thread.start()
