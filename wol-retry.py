import argparse
import socket
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument('mac_address')
parser.add_argument('ping_destination')
parser.add_argument('--retries', type=int, default=5)
parser.add_argument('--delay', type=float, default=30.0)
args = parser.parse_args()

def wol(mac_address):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.connect(('255.255.255.255', 9))
        magic_packet = bytes.fromhex('f' * 12 + mac_address.replace(':', '') * 16)
        assert sock.send(magic_packet) == len(magic_packet)

for i in range(args.retries):
    print(f'Sending magic packet to {args.mac_address}.')
    wol(args.mac_address)
    time.sleep(args.delay)
    p = subprocess.run(f'ping -c 3 {args.ping_destination}'.split())
    if p.returncode == 0:
        print(f'{args.ping_destination} is awake.')
        break
else:
    raise Exception(f"Couldn't wake {args.mac_address}.")
