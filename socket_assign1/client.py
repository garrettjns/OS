from socket import *

client_sock = socket(AF_INET, SOCK_STREAM)
try:
        client_sock.connect(("localhost", 7069))
        while True:
            server_data = client_sock.recv(16384)
            if server_data:
                print(server_data)
            else:
                client_sock.close()
                break
                   
#cannot connect to server: close client socket
except:
    print("Error connecting to server")
    client_sock.close()
        

