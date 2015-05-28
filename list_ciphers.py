#!/usr/bin/env python3
import re
import subprocess
import os
from collections import defaultdict, OrderedDict
import operator
import numpy as np
import matplotlib
matplotlib.rcParams.update({'figure.autolayout': True})
import matplotlib.pyplot as plt
from progressbar import ProgressBar

def check_output(cmd):
    raw_output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    return raw_output.decode('utf-8')

def get_top_alexa_ranking():
    tmp_filename = 'top-1m.csv.zip'
    alexa_static_link = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
    subprocess.call('curl {} -o {}'.format(alexa_static_link,tmp_filename),shell=True)
    subprocess.call('unzip -o {}'.format(tmp_filename),shell=True)
    if not os.path.isfile('top-1m.csv'):
        raise EnvironmentError

def parse_servers(filename,nmbr):
    servers = []
    with open(filename,'r') as serv_file:
        server_lines = [next(serv_file) for x in range(nmbr)]
    for line in server_lines:
        servers.append(line.strip().split(',')[1])
    return servers

def plot_histogram(hist):
    od = OrderedDict(sorted(hist.items(), key=operator.itemgetter(1)))
    N = len(od.keys())
    width = 0.8
    ind = np.arange(N)
    plt.bar(ind + width/2, [od[key] for key in od.keys()], width)
    plt.xticks(ind + width, list(od.keys()), rotation=90)
    plt.savefig("histogram.png")
    plt.close()
    
get_top_alexa_ranking()
servers = parse_servers('top-1m.csv', 100)

port = '443'
# FIXME openssl lists some ciphers twice 
ciphers = list(set(check_output('openssl ciphers ALL:eNULL').strip().split(':')))
openssl_cmd = 'echo -n | timeout 3 openssl s_client -cipher "{}" -connect "{}" 2>&1'

hist = defaultdict(int)
counter = 0
total = len(servers)

for server in servers:
    counter += 1
    pbar = ProgressBar(len(ciphers))
    print("({}/{}) Inspecting {}".format(counter, total, server))
    pbar.start()
    for idx, cipher in enumerate(ciphers):
        try:
            ret_string = check_output(openssl_cmd.format(cipher, server + ":" + port))
        except subprocess.CalledProcessError:
            pass
        else:
            hist[cipher] += 1
        pbar.update(idx+1)
    pbar.finish()

plot_histogram(hist)
