import os
import argparse
import getpass

default_proxy = 'https://autoproxy-emea.delphiauto.net:8080'
default_command = 'install'

parser = argparse.ArgumentParser(description='Script to run pip behind proxy')
parser.add_argument('package_name', help='Name of packege')
parser.add_argument('-e', '--exe', help='Pip executable, system default by default ', default='pip.exe')
parser.add_argument('-px', '--proxy', help='Proxy addres (default: {})'.format(default_proxy), default=default_proxy)
parser.add_argument('-c', '--command', help='Pip command (default: {})'.format(default_command), default=default_command)
parser.add_argument('-u', '--user', help='Proxy user', default='NO_USER')
parser.add_argument('-p', '--passwd', help='Proxy passwd', default='NO_PASS')


def main(args):
    if args.user == 'NO_USER':
        args.user = getpass.getpass('Proxy user:')
    if args.passwd == 'NO_PASS':
        args.passwd = getpass.getpass('Proxy password:')

    if 'https://' in args.proxy:
        hidden_proxy = args.proxy
        hidden_proxy = hidden_proxy[:8] + '{}:{}@'.format('****', '****') + hidden_proxy[8:]
        args.proxy = args.proxy[:8] + '{}:{}@'.format(args.user, args.passwd) + args.proxy[8:]
    elif 'http://' in args.proxy:
        hidden_proxy = args.proxy
        hidden_proxy = hidden_proxy[:7] + '{}:{}@'.format('****', '****') + hidden_proxy[7:]
        args.proxy = args.proxy[:7] + '{}:{}@'.format(args.user, args.passwd) + args.proxy[7:]
    else:
        print('Incorrect proxy address: {}\nUse http:// or https:// address.'.format(args.proxy))
        return

    print('Executing: {} {} --proxy {} {}'.format(args.exe, args.command, hidden_proxy, args.package_name))
    os.system('{} {} --proxy {} {}'.format(args.exe, args.command, args.proxy, args.package_name))
    print('Jobs done!')


if __name__ == '__main__':
    main(parser.parse_args())