#!/usr/bin/env python
# Script that reads .cloginrc credential/configuration file for clogin
from fnmatch import fnmatch

__version__ = (1,1)


class CloginSyntaxErrorException(Exception):
    pass

def read_cloginrc(router, dot_cloginrc='.cloginrc'):
    debug = True
    debug = False

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
                            # user's password and enable's secret
                            password = {'password' : chunks[3], 'enable' : chunks[4]}
                        
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
                        
                        passprompt = chunks[3]

            else:
                raise CloginSyntaxErrorException(line)
        if debug:
            print user
            print password
            print method
            print userprompt
            print passprompt
            print autoenable

        return (user, password, method, userprompt, passprompt, autoenable)




def test():
    routers = [
        'r1.custx.net',
        'r1.custy.net',
        'r1.custz.net',
        'b.r2.custx.net',
        'b.r2.custy.net',
        'b.r2.custz.net',
        'r3.cust1.net',
        'r3.cust2.net',
        'r3.cust3.net',
        'r4.net',
        'c.r4.net',
        'e.d.r5.net',
        'r4.net.pl',
        'net.pl',
        'e.d.r5.net.pl',
    ]

    for r in routers:
        user, password, method, userprompt, passprompt, autoenable = read_cloginrc(r)
        print "router={}, user={} password={} method={}".format(r, user, password, method)


if __name__ == '__main__':
    test()
