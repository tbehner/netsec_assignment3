#!/usr/bin/env python3
import socket
import ssl
from collections import defaultdict, OrderedDict
import operator
import numpy as np
import matplotlib
matplotlib.rcParams.update({'figure.autolayout': True})
import matplotlib.pyplot as plt
import os

# read file with domains, every line must contain one domain and return list of domains
def getDomainsFromFile(file_name):
    domains = []
    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            domains.append(line.strip())
    return domains

# get list of tls information (i.e. cipher suites) by connecting to the server over https
def getServerTlsInformation(domain, timeout):
    try:
        # create socket, then use ssl to connect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)

        # the file where the certificates are saved is platform dependend
        # if on your system those are saved in a different place, please add
        # the filepath to this list 
        ca_cert_files = [
                '/etc/ssl/certs/ca-bundle.crt', 
                '/etc/ssl/certs/ca-certificates.crt',
                ]
        ca_cert_file = None
        for cert_file in ca_cert_files:
            if os.path.exists(cert_file):
                ca_cert_file = cert_file
        if ca_cert_file is None:
            raise RuntimeError

        ssl_sock = ssl.wrap_socket(s, cert_reqs=ssl.CERT_REQUIRED, ca_certs=ca_cert_file)
        ssl_sock.connect((domain, 443))
        # read and return all cipher information
        return ssl_sock.cipher()
    except:
        return ["time out"]

# plot histogram of cipher information
def plot_histogram(hist):
    od = OrderedDict(sorted(hist.items(), key=operator.itemgetter(1)))
    N = len(od.keys())
    width = 0.8
    ind = np.arange(N)
    plt.bar(ind + width/2, [od[key] for key in od.keys()], width)
    plt.xticks(ind + width, list(od.keys()), rotation=90)
    plt.savefig("task_3_5_cipher_suite_histogram.png")
    plt.close()

# get list domains from Alexa Top 500 list
domains = getDomainsFromFile("alexa_top_500_domains.txt")
hist = defaultdict(int)

# analyze each domain in list and write information in file
with open("task_3_5_cipher_suite_output.txt", "w") as f:
    for domain in domains:
        print("{}/{}".format(i+1, len(domains)))
        cipher_information = getServerTlsInformation(domain, 2)
        hist[cipher_information[0]] += 1
        f.write("----------------------------------------\r\n")
        f.write("{}\r\n".format(domain))
        for info in cipher_information:
            f.write("{}\r\n".format(info))
        f.write("----------------------------------------\r\n")
        f.write("\r\n")

plot_histogram(hist)
