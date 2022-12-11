import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('user')
parser.add_argument('mac_address')
parser.add_argument('ping_destination')
parser.add_argument('--hour', default='0')
parser.add_argument('--minute', default='0')
parser.add_argument('--day', default='*')
parser.add_argument('--month', default='*')
args = parser.parse_args()

DIR = os.path.dirname(os.path.realpath(__file__))

with open('/etc/crontab', 'a') as crontab:
    crontab.write(f'{args.minute} {args.hour} {args.day} {args.month} * {args.user} systemd-cat python3 -u {DIR}/wol-retry.py {args.mac_address} {args.ping_destination}\n')
