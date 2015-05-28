#!/usr/bin/env python3
import socket
import ssl

def getDomainsFromFile(file_name):
    domains = []
    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            domains.append(line.strip())
    return domains
    
def getServerTlsInformation(domain, port, timeout):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        ssl_sock = ssl.wrap_socket(s, cert_reqs=ssl.CERT_REQUIRED, ca_certs='/etc/ssl/certs/ca-certificates.crt')
        ssl_sock.connect((domain, port))
        return ssl_sock.cipher()
    except:
        return ["time out"]

domains = getDomainsFromFile("alexa_top_500_domains.txt")
listed_domain_count = 0
with open("task_3_5_cipher_suite_output.txt", "w") as f:
    for domain in domains:
        listed_domain_count += 1
        print "%s/%s" % (listed_domain_count, len(domains))
        f.write("----------------------------------------\r\n")
        f.write("%s\r\n" % domain)
        cipher_information = getServerTlsInformation(domain, 443, 2)
        for info in cipher_information:
            f.write("%s\r\n" % info)
        f.write("----------------------------------------\r\n")
        f.write("\r\n")