from socket import *
from datetime import datetime

client_sock = socket(AF_INET, SOCK_STREAM)

try:
        client_sock.connect(("localhost", 8080))
#cannot connect to server: close client socket
except:
        print("Error connecting to server")
        client_sock.close()

start_timer = False

client_sock.setblocking(0)
counter = 0

while True:
        try: 
                server_data = client_sock.recv(4096)
                if server_data:
                        print("\nserver localhost replied at " + datetime.now().strftime('%H:%M:%S') +  ": " + \
                              server_data.decode() + "\n")
                        if "bye" not in server_data.decode():
                                try:
                                        client_sock.send(input().encode())
                                        t1 = datetime.now().strftime('%H:%M:%S')
                                        print("sent to server at : ", t1)
                                        counter = 0
                                except error:
                                        continue
                        t1 = datetime.now().strftime('%H:%M:%S')
                else:
                        print(server_data.decode())
                        client_sock.close()
                        break
        #the socket has no data yet


        except error:
                
                t2 = datetime.now().strftime('%H:%M:%S')

                sec2 = int(t2.split(":")[2])
                sec1 = int(t1.split(":")[2])
                
                elapsed = sec2 - sec1

                if elapsed > counter:
                        counter = elapsed
                        print("at ", t2, " waiting for response, "\
                              + str(elapsed) + " seconds have elapsed")
                        counter += 1
                continue
                        
'''                
        except:
                print(datetime.now().strftime('%H:%M:%S'))
        if len(server_data) > 0:
                print(server_data.decode())
                if "bye" not in server_data.decode():
                        while True:
                                send_result = client_sock.send(input().encode())
                                if send_result > 0:
                                        t1 = datetime.now().strftime('%H:%M:%S')
                                        print("sent to server at : ", t1)
                                elif send_result == 0:
                                        continue
                else:
                        client_sock.close()
                        break
        else:
                continue

'''
