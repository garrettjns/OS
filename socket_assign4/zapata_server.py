from socket import *
import time
import random

s = socket(AF_INET, SOCK_STREAM)
s.bind(("localhost", 7069))
s.listen(1)

print("Waiting for a client to connect...")
conn, addr = s.accept()
print("Connected by", addr)

# send the first question to the client
conn.send("Hello! Are you Male or Female?".encode())

while True:
    data = conn.recv(1024).decode()  # receive input from client
    if not data:
        break
    if data.lower() == "male":
        conn.send("Me too! Are you a CS major?".encode())
        start_time = time.time()
        major = conn.recv(1024).decode()  # receive input from client
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        print(f"Response delay: {elapsed_time} seconds")
        if major.lower() == "yes":
            conn.send("Excellent. I am too. Whats an animal you like and two that you dont?".encode())
            start_time = time.time()
            animals = conn.recv(1024).decode()  # receive input from client
            end_time = time.time()
            elapsed_time = round(end_time - start_time, 2)
            print(f"Response delay: {elapsed_time} seconds")
            a1, a2, a3 = animals.split()
            time.sleep(int(4*random.random()))
            conn.send((a1 + " hey me too. but i hate " + a3 + " as well. Bye for now").encode())  # send response to client
            break
        elif major.lower() == "no":
            conn.send("Too bad. Whats an animal you like and two that you dont?".encode())
            start_time = time.time()
            animals = conn.recv(1024).decode()  # receive input from client
            end_time = time.time()
            elapsed_time = round(end_time - start_time, 2)
            print(f"Response delay: {elapsed_time} seconds")
            a1, a2, a3 = animals.split()
            time.sleep(int(4*random.random()))
            conn.send((a1 + " awesome. but i hate, " + a3 + " bye for now").encode())  # send response to client
            break
        else:
            conn.send("Sorry, I don't know what you mean. Goodbye!".encode())
            break
    elif data.lower() == "female":
        conn.send("How excellent! Are you a CS major?".encode())
        start_time = time.time()
        major = conn.recv(1024).decode()  # receive input from client
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        print(f"Response delay: {elapsed_time} seconds")
        if major.lower() == "yes":
            conn.send("Excellent. I am too. Whats an animal you like and two that you dont?".encode())
            start_time = time.time()
            animals = conn.recv(1024).decode()  # receive input from client
            end_time = time.time()
            elapsed_time = round(end_time - start_time, 2)
            print(f"Response delay: {elapsed_time} seconds")
            a1, a2, a3 = animals.split()
            time.sleep(int(4*random.random()))
            conn.send((a1 + " awesome. but i hate, " + a3 + " bye for now").encode()) 
        elif major.lower() == "no":
            conn.send("Too bad. Whats an animal you like and two that you dont?".encode())
            start_time = time.time()
            animals = conn.recv(1024).decode()  # receive input from client
            end_time = time.time()
            elapsed_time = round(end_time - start_time, 2)
            print(f"Response delay: {elapsed_time} seconds")
            a1, a2, a3 = animals.split()
            time.sleep(int(4*random.random()))
            conn.send((a1 + " awesome. but i hate, " + a3 + " bye for now").encode())  # send response to client
            break
        else:
            conn.send("Sorry, I don't know what you mean. Goodbye!".encode())
            break
    else:
        conn.send("Sorry, I don't know what you mean. Goodbye!".encode())
        break
conn.send("\nThank you for chatting with me. Goodbye!".encode())
print("\nChatbot ended.")
conn.close()
s.close()
exit(0)


