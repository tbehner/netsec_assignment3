#!/usr/bin/env python3
import re
import subprocess
import os

def check_output(cmd):
    raw_output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    return raw_output.decode('utf-8')

def get_top100_alexa_ranking():
    tmp_filename = 'top-1m.zip'
    alexa_static_link = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
    subprocess.call('curl {} -o {}'.format(alex_static_link, tmp_filename))
    subprocess.call('unzip {}'.format(tmp_filename))
    if not os.path.isfile('top-1m.csv'):
        raise EnvironmentError

get_top100_alexa_ranking()
servers = ['www.uni-bonn.de', 'www.google.de']
port = '443'
ciphers = check_output('openssl ciphers ALL:eNULL').strip().split(':')
openssl_cmd = 'echo -n | openssl s_client -cipher "{}" -connect "{}" 2>&1'

for server in servers:
    print("======== {} ========".format(server))
    for cipher in ciphers:
        try:
            ret_string = check_output(openssl_cmd.format(cipher, server + ":" + port))
        except subprocess.CalledProcessError:
            continue
        else:
            print("{}".format(cipher))
    print("\n\n\n")

