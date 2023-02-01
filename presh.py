#!/usr/bin/python3

import os

commands = {'prog1' : ['/usr/bin/cat', ('cat', '/proc/cpuinfo')],
            'prog2' : ['/usr/bin/echo', ('echo', 'Hello World')],
            'prog3' : ['/cygdrive/c/cs_4375/pre-shell/spinner.py', ("./spinner.py","1000000")],
            'prog4' : ["/usr/bin/uname", ("uname", "-a")],
            'prog5' : ['/cygdrive/c/cs_4375/pre-shell/spinner.py', ("./spinner.py","2000000" + ' &')]}


count = 1
while count < 6:
    pid = os.fork()
    if pid < 0:
        print("Error forking")
    elif pid == 0:
        print(count)
        command = commands['prog' + str(count)][0]
        args = commands['prog' + str(count)][1]
        os.execv(command, args)
    else:
        os.wait()        
    count += 1



