from socket import *

client_sock = socket(AF_INET, SOCK_STREAM)

try:
        print("connecting...")
        client_sock.connect(("nigelward.com", 80))
#cannot connect to server: close client socket
except:
        print("Error connecting to server")
        client_sock.close()
        exit()

http_request = "GET /index.html HTTP/1.1\r\nHost: nigelward.com \r\n\r\n"
client_sock.send(http_request.encode(), 80)
server_data = client_sock.recv(16384)
print(server_data[1001:1011])
print(server_data[2001:2011])
client_sock.close()
