#!/usr/bin/python3

import os, sys, re

def cd(inp):

    try:
    
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
            
    except FileNotFoundError:

        print("Path not found")
        
    return

            
def split_args (inp):
    
    # the program has arguments

    if re.match('\w+\s+(-{1,2})?\'?\w+\'?(\.?\w+)*', inp):    

        command, arguments = inp.split(maxsplit=1)

        command = command.strip()

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

    args = tuple(args)        

    return path, args, found


use_file = False
lines=[]
count = 0

# check for file as argument to argv

if len(sys.argv) == 2:
    use_file = True
    filename = sys.argv[1]
    try:
        fp = open(filename, 'r')
        lines = fp.readlines()
        lines = [line.rstrip() for line in lines if line.strip() and '#' not in line]
        print(lines)
    except FileNotFoundError:
        print("File Not Found: " + sys.argv[1])

while True:

    prog_found = True
    pipe_flag = False
    bg_enabled = False
    in_redirect = False
    out_redirect = False
    filename = ""

       
    print(os.getcwd())
    
    if os.environ['PS1'] == "" or os.environ['PS1'] is None:
                       
        os.environ['PS1'] = "$$$$"
                       
    PS1 = os.environ['PS1']

    if not use_file:
        inp = input(PS1 + " ")
    else:
        try:
            inp = lines[count]
            count += 1
        except:
            use_file = False
            continue
        
    if 'quit' in inp:
        exit()

    # check for partial cd match

    if re.match('\s*([^a-z\d\\.\*]+)?cd\s*', inp):
        cd(inp)
        continue

    if '&' in inp:
        bg_enabled = True
        inp = inp.strip('&').strip()
        cmd = inp  
    
    if '|' in inp:
        pipe_flag = True
        cmd1, cmd2 = inp.split('|')
        path, args, prog_found = split_args(cmd1)
        path2, args2, prog_found2 = split_args(cmd2)

        stdin = os.dup(0)
        stdout = os.dup(1)
        
        if not prog_found or not prog_found2:
            print("Error - Program not found")
            continue
     
    elif '>' in inp:
        stdout = os.dup(1)
        out_redirect = True
        cmd, filename = inp.split('>')
        path, args, prog_found = split_args(cmd)
        cmd = cmd.strip()
        filename = filename.strip()
        os.close(1)
        os.open(filename, os.O_WRONLY | os.O_CREAT)
        os.set_inheritable(1, True)
        
    elif '<' in inp:
        stdin = os.dup(0)
        in_redirect = True
        cmd, filename = inp.split('<')
        path, args, prog_found = split_args(cmd)
        cmd = cmd.strip()
        filename = filename.strip()
        os.close(0)
        os.open(filename, os.O_RDONLY)
        os.set_inheritable(0, True)
            
    else:
        cmd = inp.strip()
        path, args, prog_found = split_args(cmd)

    if not prog_found:
        print("Error - Program not found")
        continue
    
    if pipe_flag:
        r, w = os.pipe()
        os.set_inheritable(r, True)
        os.set_inheritable(w, True)
        
        c1 = os.fork()
        
        if c1 < 0:
            print("Error forking")
            
        if c1 == 0:
            os.close(r)
            os.dup2(w,1) #process writes to file descriptor w
            rc = os.execv(path, args)
            
            if rc != 0:
                print("Program terminated: exit code " + rc)
    
        c2 = os.fork()

        if c2 == 0:
            os.close(w)
            os.dup2(r,0) #connect read end of pipe to stdin
            
            rc = os.execv(path2, args2)
            if rc != 0:
                print("Program terminated: exit code " + rc)

        if bg_enabled:
            print("bg enabled")
            os.close(r)
            os.close(w)

            os.dup2(stdin, 0)
            os.dup2(stdout, 1)
        else:
            os.wait()
            
            os.close(r)
            os.close(w)
            
            os.dup2(stdin, 0)
            os.dup2(stdout, 1)
            
            input()
    else:
        cpid = os.fork()

        if cpid < 0:
            print("Error forking")

        elif cpid == 0:                       
            rc = os.execv(path, args)
            if rc != 0:
                print("Program terminated: exit code " + rc)
        
        if bg_enabled:
            print("bg enabled")
        else:
            os.wait()

        if out_redirect:
            os.dup2(stdout, 1)
                       
        if in_redirect:
            os.dup2(stdin, 0)


