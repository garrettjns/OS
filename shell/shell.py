#!/usr/bin/python3


#  [line.rstrip() for line in fp if line.strip()]


import os, sys, re

commands = {'prog1' : ['/usr/bin/cat', ('cat', '/proc/cpuinfo')],
            'prog2' : ['/usr/bin/echo', ('echo', 'Hello World')],
            'prog3' : ['/cygdrive/c/cs_4375/pre-shell/spinner.py', ("./spinner.py","1000000")],
            'prog4' : ["/usr/bin/uname", ("uname", "-a")],
            'prog5' : ['/cygdrive/c/cs_4375/pre-shell/spinner.py', ("./spinner.py","2000000", ' &')]}


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
    
    path, args, prog_found = split_args(inp)

    if not prog_found:
        print("Error - Program not found")
        continue

    pid = os.fork()

    if pid < 0:
        print("Error forking")
    elif pid == 0:
        print(args)
        rc = os.execv(path, args)
        if rc != 0:
            print("Program terminated: exit code " + rc)
    else:
        os.wait()        
    
