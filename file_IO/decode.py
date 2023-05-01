#!/usr/bin/python3
# decode.py
import sys, time, os
bufferSize = 512
key = b'uteputep'


def processUtep(occurrence):
    global payloadLength, codeFile
    if occurrence == 2:
        payloadLength = int(f.read(3))  # a 3-digit number
        print('payloadLength is %d' % payloadLength)
        return True
    elif occurrence == 4:
        print('the secret is `%s\' ' % f.read(payloadLength).decode())
        global start_time
        end_time = time.time()
        # calculate the CPU + I/O time
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.4f} seconds")
        exit(0)
    else:
        return None


def seekUtepInBuffer(buffer, f, switch):
    global key
    bufferLen = len(buffer)
    if not switch:  # search forwards in buffer
        for i in range(bufferLen - len(key)):
            if buffer[i] == key[0]:
                if buffer[i:i+len(key)] == key:
                    print(buffer[i:i+len(key)+5])
                    print('spotted %s at %d ' % (key, i))
                    f.seek(len(key) + i - bufferLen, 1)  # seek backwards
                    return True
        f.seek(-len(key), 1)
    else:   # search backwards in buffer
        for i in range(bufferLen - 1, 6, -1):
            if buffer[i] == key[7]:
                if buffer[i-len(key)+1:i+1] == key:
                    print(buffer[i-len(key)+1:i+5] )
                    print('spotted %s at %d ' % (key, i))
                    f.seek(i - bufferLen + 1, 1)  # seek backwards
                    return True
        f.seek(-(2*bufferLen) + len(key), 1)
        return False

start_time = time.time()
if len(sys.argv) < 2:
    print("usage: utepDecode filename")
    exit(-1)
codeFile = sys.argv[1]
keysSeen = 0
switchSeek = False
switch = False
file_size = os.path.getsize(codeFile)
with open(codeFile, 'rb') as f:
    if file_size < bufferSize:
        bufferSize = file_size
    while (1):
        if switchSeek:
            f.seek(-bufferSize, 2)  # start reading from the end of the file
            switch = True
            switchSeek = False
        buffer = f.read(bufferSize)
        if buffer == b'':  # end of file
            exit(0)
        if seekUtepInBuffer(buffer, f, switch):
            keysSeen += 1
            switchSeek = processUtep(keysSeen)
            if switch and f.tell() <= bufferSize:
                bufferSize = f.tell() - 8  # subtract length of key
                f.seek(0, 0)
            elif switch:
                f.seek(-bufferSize - len(key), 1)
                
