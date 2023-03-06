from socket import *

client_sock = socket(AF_INET, SOCK_STREAM)
try:
        client_sock.connect(("localhost", 7069))
#cannot connect to server: close client socket
except:
        print("Error connecting to server")
        client_sock.close()

while True:
        server_data = client_sock.recv(16384)
        if server_data:
                print(server_data)
                print(int.from_bytes(server_data, byteorder="big"))
        else:
                client_sock.close()
                break
                   
        

