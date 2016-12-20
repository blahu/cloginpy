#!/usr/bin/env python
# netmiko-powered clogin alternative

from netmiko import ConnectHandler
from fnmatch import fnmatch
import argparse
import sys

class CloginSyntaxErrorException(Exception):
    pass

def read_cloginrc(router, dot_cloginrc='.cloginrc'):
    debug = False
    debug = True

    if debug:
        print
        print ">>>> read_cloginrc(router={})<<<<".format(router)
        print

    user = ''
    user_found = 0
    password = ''
    password_found = 0
    method = ['telnet', 'ssh']
    method_found = 0
    userprompt = '{"(Username|login|user name):"}'
    userprompt_found = 0
    passprompt = '"([Pp]assword|passwd):"'
    passprompt_found = 0
    autoenable = 1
    autoenable_found = 0

    with open(dot_cloginrc) as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue
            if '#' in line[0]:
                continue

            #if debug:
            #    print line

            # split line into chunks (could be variable)
            chunks = line.split()

            if debug:
                print chunks
            
            if chunks[0] == 'add':

                ## USER
                if chunks[1] == 'user' and not user_found:
                    if fnmatch(router, chunks[2]):
                        user_found = 1
                        
                        if debug:
                            print "{}_found = {}".format(chunks[1], user_found)
                        
                        user = chunks[3]
                
                ## PASSWORD
                if chunks[1] == 'password' and not password_found:
                    if fnmatch(router, chunks[2]):
                        password_found = 1
                        
                        if debug:
                            print "{}_found = {}".format(chunks[1], password_found)
                        
                        if len(chunks) == 4:
                            # user's password only
                            password = {'password' : chunks[3]}

                        elif len(chunks) == 5:
                            # user's password andsecret's secret
                            password = {'password' : chunks[3], 'secret' : chunks[4]}
                        
                        else:
                            # reset flag if more than 2 passwords
                            password_found = 0
                        
                            if debug:
                                print "Too many passwords"
                        

                ## METHOD
                if chunks[1] == 'method' and not method_found:
                    if fnmatch(router, chunks[2]):
                        method_found = 1
                        
                        if debug:
                            print "{}_found = {}".format(chunks[1], method_found)
                        
                        if len(chunks) == 4:
                            # one method only
                            method = [chunks[3]]

                        elif len(chunks) == 5:
                            # two methods defined
                            method = [chunks[3], chunks[4]]
                        
                        else:
                            # reset flag if more than 2 methods
                            method_found = 0

                            if debug:
                                print "Too many methods"
                
                ## USERPROMPT
                if chunks[1] == 'userprompt' and not userprompt_found:
                    if fnmatch(router, chunks[2]):
                        userprompt_found = 1
                        
                        if debug:
                            print "{}_found = {}".format(chunks[1], userprompt_found)
                        
                        userprompt = chunks[3]
                
                ## PASSPROMPT
                if chunks[1] == 'passprompt' and not passprompt_found:
                    if fnmatch(router, chunks[2]):
                        passprompt_found = 1
                        
                        if debug:
                            print "{}_found = {}".format(chunks[1], passprompt_found)
                        
                        passprompt = chunks[3]

                ## AUTOENABLE
                if chunks[1] == 'autoenable' and not autoenable_found:
                    if fnmatch(router, chunks[2]):
                        autoenable_found = 1
                        
                        if debug:
                            print "{}_found = {}".format(chunks[1], autoenable_found)
                        
                        autoenable = int(chunks[3])

            else:
                raise CloginSyntaxErrorException(line)
    if debug:
        print user
        print password
        print method
        print userprompt
        print passprompt
        print autoenable

    return (user, password, method, autoenable)

def run_commands(cmds, autoenable, **device):
    debug = True
    if debug:
        print cmds
        print autoenable
        print device

    conn = ConnectHandler(**device)
    if not autoenable:
        if debug:
            print "Enabling"
        conn.enable()
    else:
        print "aaa"

    prompt = conn.find_prompt()
    for c in cmds.split(';'):
        c = c.strip()
        output = conn.send_command(c)
        print prompt + ' ' + c
        print output

    conn.disconnect()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--commands', help='commands, use semicolon ";" to separate', type=str)
    parser.add_argument('-t', '--timeout', help='timeout in seconds', type=int, default=8)
    parser.add_argument('-p', '--port', help='tcp port to connect to', type=int, default=22)
    parser.add_argument('-d', '--device_type', help='device type as per ' + 
            'https://github.com/ktbyers/netmiko/blob/master/netmiko/ssh_dispatcher.py#L34', type=str, default='cisco_ios')
    parser.add_argument('router', help='Please specify router to execute commands', type=str)
    args = parser.parse_args()

    host = args.router
    port = args.port

    try:
        user, password, method, autoenable =  read_cloginrc(args.router)
    except CloginSyntaxErrorException as e:
        print ".cloginrc syntax error at this line [{}]".format(e)
        sys.exit(1)

    if not user or not password:
        print "{} not found in .cloginrc".format(args.router)
        sys.exit(2)

    try:
        secret = password['secret']
    except KeyError as e:
        secret = ''

    ## password dict becomes password str
    password = password['password']

    ## in .cloginrc password and secrets are in curly brackets, need to get rid of them
    secret = secret.strip('{}')
    password = password.strip('{}')

    a_device = {
        'device_type' : args.device_type,
        'host' : host,
        'port' : port,
        'username' : user,
        'password' : password,
        'secret' : secret,
        #'global_delay_factor' : 7,
        'timeout' : args.timeout,
    }
    print ">>>>> {}:{} <<<<<".format(a_device['host'], a_device['port'])
    run_commands(cmds=args.commands, autoenable=autoenable, **a_device)
    print ">>>>> END <<<<<"
    print

