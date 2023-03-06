from socket import *

client_sock = socket(AF_INET, SOCK_STREAM)
try:
        client_sock.connect(("localhost", 8080))
#cannot connect to server: close client socket
except:
        print("Error connecting to server")
        client_sock.close()

while True:
        server_data = client_sock.recv(4096)
        if server_data:
                print(server_data.decode())
                if "bye" not in server_data.decode():
                        client_sock.send(input().encode())
        else:
                client_sock.close()
                break
                   
        

