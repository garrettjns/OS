from socket import *
import datetime

s = socket(AF_INET, SOCK_STREAM)
s.connect(("localhost", 8080))

s.setblocking(0)

while True:
    start_time = datetime.datetime.now()
    try:
        data = s.recv(1024).decode()
    except error:
        t1 = datetime.datetime.now()
        while True:
            t2 = datetime.datetime.now()
            if (t2 - t1).seconds >= 1:
                print(f"waiting for response, {(t2 - start_time).seconds} seconds have elapsed")
                t1 = t2
            try:
                data = s.recv(1024).decode()
                break
            except error:
                pass
    end_time = datetime.datetime.now()
    if "bye" in data:
        print(data)
        break
    elif not data:
        break
    
    print(f"Received response in {(end_time - start_time).total_seconds():.1f} seconds")
    print(data)

    response = input()  # get response from user
    s.send(response.encode())  # send response to server

print("\nClosing connection...")
s.close()
print()
