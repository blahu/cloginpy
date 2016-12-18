#!/usr/bin/env python
# netmiko-powered clogin alternative

from netmiko import ConnectHandler


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
    parser.add_argument('-c', '--commands', help='Please specify commands, use semicolon ";" to separate', type=str)
    parser.add_argument('router', help='Please specify router to execute commands', 
            type=str,
            nargs='?',
            default='_')
    args = parser.parse_args()

    if args.router is not '_':
        try:
            ip, port = args.router.split(':')
        except ValueError:
            ip = args.router
            port = 22
        a_device = {
            'device_type' : 'arista_eos',
            'ip' : ip,
            'port' : port,
            'username' : 'admin',
            'password' : 'admin',
            'global_delay_factor' : 7,
        }
        print ">>>>> {}:{} <<<<<".format(a_device['ip'], a_device['port'])
        run_commands(cmds=args.commands, **a_device)
        print ">>>>> END <<<<<"
        print
    else:
        test()

