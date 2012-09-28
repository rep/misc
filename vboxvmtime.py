#!/usr/bin/python
# -*- coding: utf8 -*-

__author__ = "Mark Schloesser"
__copyright__ = "Copyright 2012, Mark Schloesser"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "ms@mwcollect.org"


import sys, subprocess, datetime

def usage():
	print '''Usage: {0} <vmname> <mm/dd/yyyy>
\tsets <vmname>\'s bios offset so that its system time is <mm/dd/yyyy>'''.format(sys.argv[0])
	sys.exit(2)

if len(sys.argv) != 3:
	usage()

try:
	orig = datetime.datetime.strptime(sys.argv[2], '%m/%d/%Y').date()
except:
	print 'Error: could not parse supplied date. Format: mm/dd/yyyy'
	sys.exit(2)

today = datetime.datetime.now().date()
diffdays = (today - orig).days
diffmsecs = diffdays * 24 * 60 * 60 * 1000

print 'Offset: {0} msecs'.format(diffmsecs)

try:
	proc = subprocess.Popen(["VBoxManage", "modifyvm", sys.argv[1], "--biossystemtimeoffset", "-{0}".format(diffmsecs)], 
		stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = proc.communicate()
	retcode = proc.poll()
except Exception, e:
	print 'Error: VBoxManage failed, exception {0}'.format(e)
	sys.exit(2)

if retcode != 0:
	print stderr
	sys.exit(2)

print 'Succeeded!'
sys.exit(0)

