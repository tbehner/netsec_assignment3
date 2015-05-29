"""
Minimal DNS sniffer for Python 2.

Note that this is just a minimal example to get you started and not a perfect 
solution. There are some parts which definitely require change!
"""

import signal
import sys
from scapy.all import sniff


def handle_sigint(signum, frame):
    print '\nExiting...'
    sys.exit(0)


def print_packet(packet):
    packet.show()


def start_sniffing():
    signal.signal(signal.SIGINT, handle_sigint)
    print 'Starting to sniff. Hit Ctrl+C to exit...'
    sniff(filter='udp and port 53', prn=print_packet)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    start_sniffing()


if __name__ == '__main__':
    main()
