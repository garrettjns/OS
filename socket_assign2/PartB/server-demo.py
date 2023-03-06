#!/usr/bin/env python3
from socket import *
import time
s = socket(AF_INET, SOCK_STREAM)
s.bind(("localhost", 7069))
s.listen(5)
while True:
    c,a = s.accept()
    print("Received connection from" , a)
    print((256).to_bytes(2, byteorder="big"))
    c.send((256).to_bytes(2, byteorder="big"))
    c.close()

    


