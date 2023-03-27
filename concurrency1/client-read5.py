#!/usr/bin/env python3
from socket import *
s = socket(AF_INET, SOCK_STREAM)
s.connect(("localhost", 7069))
result1 = s.recv(512)
print(result1)
result2 = s.recv(512)
print(result2)
result3 = s.recv(512)
print(result3)
result4 = s.recv(512)
print(result4)
result5 = s.recv(512)
print(result5)

