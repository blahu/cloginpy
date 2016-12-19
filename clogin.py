#!/usr/bin/env python
# netmiko-powered clogin alternative

from netmiko import ConnectHandler
from cloginrc import read_cloginrc

def run_commands(cmds, **device):
    conn = ConnectHandler(**device)
    prompt = conn.find_prompt()

    for c in cmds.split(';'):
        c = c.strip()
        output = conn.send_command(c)
        print prompt + ' ' + c
        print output

    conn.disconnect()


def test():
    a_device = {
        'device_type' : 'arista_eos',
        'ip' : '127.0.0.1',
        'port' : 2221,
        'username' : 'admin',
        'password' : 'admin',
        'global_delay_factor' : 7,
    }
    cmds = 'show uptime; show clock; show version'

    print ">>>>> {}:{} <<<<<".format(a_device['ip'], a_device['port'])
    run_commands(cmds=cmds, **a_device)
    print ">>>>> END <<<<<"
    print
    
    a_device = {
        'device_type' : 'arista_eos',
        'ip' : '127.0.0.1',
        'port' : 2222,
        'username' : 'admin',
        'password' : 'admin',
        'global_delay_factor' : 7,
    }
    cmds = 'show uptime; show clock; show version'

    print ">>>>> {}:{} <<<<<".format(a_device['ip'], a_device['port'])
    run_commands(cmds=cmds, **a_device)
    print ">>>>> END <<<<<"
    print
    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--commands', help='commands, use semicolon ";" to separate', type=str)
    parser.add_argument('-t', '--timeout', help='timeout in seconds', type=int, default=8)
    parser.add_argument('-d', '--device_type', help='device type as per ' + 
            'https://github.com/ktbyers/netmiko/blob/master/netmiko/ssh_dispatcher.py#L34', type=str, default='cisco_ios')
    parser.add_argument('router', help='Please specify router to execute commands', type=str, nargs='?', default='_')
    args = parser.parse_args()

    if args.router is not '_':
        try:
            ip, port = args.router.split(':')
        except ValueError:
            ip = args.router
            port = 22
        a_device = {
            'device_type' : args.device_type,
            'ip' : ip,
            'port' : port,
            'username' : 'admin',
            'password' : 'admin',
            #'global_delay_factor' : 7,
            'timeout' : args.timeout,
        }
        print ">>>>> {}:{} <<<<<".format(a_device['ip'], a_device['port'])
        run_commands(cmds=args.commands, **a_device)
        print ">>>>> END <<<<<"
        print
    else:
        test()

