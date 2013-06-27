#!/usr/bin/python

import sys
import os
import struct

from scapy.all import IP, TCP, send, sniff

IFACE = "vboxnet0"
MYIP = "192.168.56.1"
IGNORE_PORTS = [22,]

def rand32():
	return struct.unpack("I", os.urandom(4))[0]

def iptables_drop_resets():
	os.system("iptables -A OUTPUT -o {0} -p tcp -s {1} --tcp-flags RST RST -j DROP".format(IFACE, MYIP))

def main():
	iptables_drop_resets()

	def pcb(p):
		if not p.haslayer(TCP):
			return

		ipl = p.getlayer(IP)
		tcpl = p.getlayer(TCP)

		print p.summary()

		if tcpl.flags == 2 and ipl.dst == MYIP and not tcpl.dport in IGNORE_PORTS:
			print "SYN from", ipl.src, tcpl.sport, "to port", tcpl.dport
			rp = IP(src=ipl.dst, dst=ipl.src, flags='DF', id=0)/TCP(sport=tcpl.dport, dport=tcpl.sport, ack=tcpl.seq+1, seq=rand32(), flags="SA")
			send(rp)

	# for some reason the bpf does not work sometimes...
	ps = sniff(store=0, iface=IFACE, prn=pcb, filter="tcp")

	return 0

if __name__ == "__main__":
	try: sys.exit(main())
	except KeyboardInterrupt: pass
