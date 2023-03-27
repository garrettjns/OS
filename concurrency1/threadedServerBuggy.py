#!/usr/bin/env python3
from socket import *
import datetime, time, random
import threading

# Why is the count of cumulativeResponses often less than the sum of
#   the per-Thread sends?  For example, this is common when many
#   clients simultaneously connect.  This has to be fixed!!!

lock = threading.Lock()

def clientHandler(clientSocket, address, threadNumber):
    global cumulativeResponses
    myResponses = 0
    print("I'm a new thread, number %d" % threadNumber)
    print("  handling communications with " , address)
    for x in range(1,5):  # blast 5 strings to the client 
        lock.acquire()
        oldCumulativeResponses = cumulativeResponses
        time.sleep(5)
        time1 = time.time()
        nowtime = datetime.datetime.now()
        toSendString = "hello from " + gethostname() + nowtime.strftime(" %A %I:%M")
        toSendBytes = toSendString.encode()
        clientSocket.send(toSendBytes)
        cumulativeResponses = oldCumulativeResponses + 1
        lock.release()
        myResponses = myResponses + 1
        print("Thread %d has done %d sends; all threads %d" %
              (threadNumber,myResponses, cumulativeResponses))
    clientSocket.close()
    return


##### main #####
nThreads = 0 
global cumulativeResponses
cumulativeResponses = 0
s = socket(AF_INET, SOCK_STREAM)
s.bind(("localhost", 7069))
s.listen(5)
while True:
    nThreads = nThreads + 1
    c,a = s.accept()
    thread = threading.Thread(target=clientHandler, args =(c,a, nThreads))
    thread.start()
s.close()



