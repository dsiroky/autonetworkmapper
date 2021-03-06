#!/usr/bin/python3

import os
import re
import sys
import ipaddress
import argparse
from subprocess import Popen, PIPE

from thirdparty import ping

#############################################################################
#############################################################################

def run_cmd(cmd):
    process = Popen(cmd, stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    return output

#############################################################################

def scan_all(network):
    ipn = ipaddress.ip_network(network)
    result = ping.multi_ping_query([str(ip) for ip in ipn.hosts()])
    return [h for (h, tm) in result.items() if tm is not None]

#############################################################################

def traceroute(ip):
    troute = run_cmd(["traceroute", "-w 1", "-n", ip]).decode("utf-8")
    trace = []
    for line in troute.split("\n"):
        m = re.match(r"\s*\d+\s+(\S+)", line)
        if m:
            host = m.group(1)
            if host != "*":
                trace.append(host)
    trace.append(ip)
    return trace

#############################################################################

def run(args):
    with open(args.output, "w") as fw:
        for host in scan_all(args.network[0]):
            print(host)
            tr = traceroute(host)
            for i in range(len(tr) - 2):
                fw.write("\"%s\" -- \"%s\";\n" % (tr[i], tr[i + 1]))

#############################################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", type=str, required=True,
                   help="output file, e.g. 'subnet1.pairs'")
    parser.add_argument("network", metavar="address", type=str, nargs=1,
                   help="network address to scan, e.g. '192.168.0.0/16'")
    args = parser.parse_args()
    run(args)
