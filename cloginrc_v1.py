#!/usr/bin/env python
# Script that reads .cloginrc credential/configuration file for clogin
__version__ = (1, 0)

from __future__ import with_statement # This isn't required in Python 2.6
from collections import OrderedDict

dot_cloginrc = '.cloginrc'

class LastUpdatedOrderedDict(OrderedDict):
    'Store items in the order the keys were last added'

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        OrderedDict.__setitem__(self, key, value)

## GLOBALS
passwords = LastUpdatedOrderedDict()
users = LastUpdatedOrderedDict()
methods = LastUpdatedOrderedDict()

def read_cloginrc():
    debug = False

    with open(dot_cloginrc) as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue
            if '#' in line[0]:
                continue

            if debug:
                print line

            # split line into chunks (could be variable)
            chunks = line.split()

            if debug:
                print chunks
            
            if chunks[0] == 'add':

                ## USERS DB
                if chunks[1] == 'user':
                    users[chunks[2]] = chunks[3]
                
                ## PASSWORDS DB
                if chunks[1] == 'password':
                    # only user's password
                    if len(chunks) == 4:
                        passwords[chunks[2]] = {'password' : chunks[3]}

                    # user's password and enable's secret
                    elif len(chunks) == 5:
                        passwords[chunks[2]] = {'password' : chunks[3], 'enable' : chunks[4]}

                ## METHODS DB
                if chunks[1] == 'method':
                    # only 1 method
                    if len(chunks) == 4:
                        methods[chunks[2]] = [chunks[3]]

                    # two methods defined
                    elif len(chunks) == 5:
                        methods[chunks[2]] = [chunks[3], chunks[4]]
        if debug:
            print users
            print passwords
            print methods

def main():
    
    read_cloginrc()

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


    import fnmatch

    for r in routers:
        found = 0
        for k,v in users.iteritems():
            if fnmatch.fnmatch(r, k):
                print "router={}, user={}".format(r, v)
                found = 1
                break

        if not found:
            print "router={}, user={}".format(r, 'NOT_FOUND')


if __name__ == '__main__':
    main()
