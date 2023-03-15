from socket import *
from datetime import datetime

client_sock = socket(AF_INET, SOCK_STREAM)

try:
        client_sock.connect(("localhost", 7069))
#cannot connect to server: close client socket
except:
        print("Error connecting to server")
        client_sock.close()


client_sock.setblocking(0)

counter = 0

#initialize t1
t1 = datetime.now().strftime('%H:%M:%S')
while True:
        try:
                server_data = client_sock.recv(4096)
                if server_data:
                        print("\nserver localhost replied at " + datetime.now().strftime('%H:%M:%S') +  ": " + \
                              server_data.decode() + "\n")
                        if "bye" not in server_data.decode():
                                try:
                                        response = input()
                                        while not response:
                                                print("Please enter valid input\n")    
                                                response = input()
                                        client_sock.send(response.encode())
                                        t1 = datetime.now().strftime('%H:%M:%S')
                                        print("sent to server at : ", t1)
                                        counter = 0
                                except error:
                                          continue
                        else:
                                client_sock.close()
                                break
        #the socket has no data yet
        except error:
                t2 = datetime.now().strftime('%H:%M:%S')

                sec2 = int(t2.split(":")[2])
                sec1 = int(t1.split(":")[2])

                
                elapsed = sec2 - sec1
                
                if elapsed > counter:
                        print("at ", t2, " waiting for response, "\
                              + str(elapsed) + " seconds have elapsed")
                        counter += 1
                continue
