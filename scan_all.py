import os
import re
import sys
from subprocess import Popen, PIPE

from thirdparty import ping

def run_cmd(cmd):
    process = Popen(cmd, stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    return output

def scan_all():
    hosts = []
    for i in range(1, 256):
        hosts.append("10.109.255.%i" % i)
    result = ping.multi_ping_query(hosts)
    return [h for (h, tm) in result.items() if tm is not None]

def traceroute(ip):
    troute = run_cmd(["traceroute", "-w 1", "-n", ip])
    trace = []
    for line in troute.split("\n"):
        m = re.match(r"\s*\d+\s+(\S+)", line)
        if m:
            host = m.group(1)
            if host != "*":
                trace.append(host)
    trace.append(ip)
    return trace

def run():
    print "graph net {"
    for host in scan_all():
        tr = traceroute(host)
        for i in range(len(tr) - 2):
            print "  \"%s\" -- \"%s\";" % (tr[i], tr[i + 1])
    print "}"

if __name__ == "__main__":
    run()
