from socket import *
import time

s = socket(AF_INET, SOCK_STREAM)
s.connect(("localhost", 7069))

while True:
    data = s.recv(1024).decode()
    if "Thank you" in data:
        print(data)
        break
    elif not data:
        break
    print(data)

    # get response time
    start_time = time.time()

    response = input()  # get response from user
    s.send(response.encode())  # send response to server

    # calculate and report delay
    end_time = time.time()
    delay = end_time - start_time
    print(f"Sent to server at {time.strftime('%H:%M:%S', time.localtime(start_time))}")
    print(f"At {time.strftime('%H:%M:%S', time.localtime(end_time))}, waiting for response, {delay:.1f} seconds have elapsed")

print("\nClosing connection...")
s.close()
print()
