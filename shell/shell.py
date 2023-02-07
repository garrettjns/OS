#!/usr/bin/python3


#  [line.rstrip() for line in fp if line.strip()]


import os, sys, re

commands = {'prog1' : ['/usr/bin/cat', ('cat', '/proc/cpuinfo')],
            'prog2' : ['/usr/bin/echo', ('echo', 'Hello World')],
            'prog3' : ['/cygdrive/c/cs_4375/pre-shell/spinner.py', ("./spinner.py","1000000")],
            'prog4' : ["/usr/bin/uname", ("uname", "-a")],
            'prog5' : ['/cygdrive/c/cs_4375/pre-shell/spinner.py', ("./spinner.py","2000000", ' &')]}
prog_found = True
pipe_flag = False

def cd(inp):

    #navigate to home
    
    if re.fullmatch('\s*([^a-z\d\\.\*]+)?cd\s*', inp):

        os.chdir(os.environ['HOME'])

    #navigate up one directory
    
    elif re.fullmatch('\s*([^a-z\d\\.\*]+)?cd\s*(\.\.){1}/?\s*', inp):
        
        path = os.getcwd()

        path = re.sub(r'/([^/]*)$', '', path)

        os.chdir(path)

    #navigate to specified path
    
    elif re.fullmatch('\s*([^a-z\d\\.\*]+)?cd\s*\/?\w*\d*(\/\w*\d*)*\/?', inp):

        command, path = inp.split()

        os.chdir(path)

    #go up one directory then down into specified path
    
    elif re.fullmatch('\s*([^a-z\d\\.\*]+)?cd\s*(\.\.){1}(/[^\/]*)+', inp):

        
        path = os.getcwd()

        path = re.sub(r'/([^/]*)$', '', path)

        os.chdir(path)

        path = re.sub('\s*([^a-z\d\\.\*]+)?cd\s*(\.\.){1}\/?', '', inp)

        os.chdir(path)

        

        
    return
'''
command, path = inp.split(maxsplit=1)

# path ends in '/'

if re.fullmatch()

# path does not end in '/'
'''
    

    
            
def split_args (inp):
    
    # the program has arguments

    if re.match('\w+\s+(-{1,2})?\'?\w+\'?(\.?\w+)*', inp):    

        command, arguments = inp.split(maxsplit=1)

        command.strip()

        arg_list = arguments.split()

        #unpack arguments into tuple form for execv()
        
        args = (*arg_list,)
        
    #the program does not have arguments

    else:
        
        command = inp.strip()

        args = ()

    PATH = os.environ['PATH']

    #check path for program

    found = False
    
    for path in PATH.split(':'):
        path = path + '/' + command
        if os.path.isfile(path):
            found = True
            break

    #package command and arguments together for execv

    args = list(args)

    args.insert(0, command)

    #TODO: strip quotes from args
    '''
    print("-----> ", repr(args))
    for arg in args:
        print(repr(arg))
        arg = arg.replace("'",'')
        print(repr(arg))
    '''
    args = tuple(args)        

    return path, args, found


while True:

    print(os.getcwd())
    
    os.environ['PS1'] = "$$$$"
    PS1 = os.environ['PS1']

    inp = input(PS1 + " ")

    if 'quit' in inp:
        exit()

    # check for partial cd match

    if re.match('\s*([^a-z\d\\.\*]+)?cd\s*', inp):
        
        cd(inp)
        continue

    if '|' in inp:
        pipe_flag = True
        cmd1, cmd2 = inp.split('|')
        path, args, prog_found = split_args(cmd1)
        path2, args2, prog_found2 = split_args(cmd2)
        print(path2, args2, prog_found2)
        print(path, args, prog_found)
    else:
        path, args, prog_found = split_args(inp)

    if not prog_found:
        print("Error - Program not found")
        continue
    if pipe_flag:
        
        r, w = os.pipe()
        
        inheritable = True
        os.set_inheritable(r, inheritable)
        os.set_inheritable(w, inheritable)
        c1 = os.fork()
        
        if c1 < 0:
            print("Error forking")
        if c1 == 0:
            os.close(1)
            os.dup(w) #process writes to file descriptor w
            '''
            os.close(0)
            os.close(2)
            os.close(3)
            os.close(4)
            '''
            rc = os.execv(path, args)
            if rc != 0:
                print("Program terminated: exit code " + rc)
                exit()
                
                exit()
        os.wait()
    
        c2 = os.fork()

        if c2 == 0:
            os.close(0)
            os.dup(w) #connect read end of pipe to stdin
            #close extra connections
            '''
            os.close(2)
            os.close(3)
            os.close(4)
            '''
            rc = os.execv(path2, args2)
            if rc != 0:
                print("Program terminated: exit code " + rc)
        os.wait()
    else:
        cpid = os.fork()

        if cpid < 0:
            print("Error forking")
        elif cpid == 0:
            print("Child ID is: ", os.getpid())
            rc = os.execv(path, args)
            if rc != 0:
                print("Program terminated: exit code " + rc)
                exit()
        
        os.wait()

            #print(rc)
            #pid, status = os.waitpid(cpid, os.WNOHANG)

            #print("-----> ", pid)
        
            #print(pid)

            #print(status)
    
