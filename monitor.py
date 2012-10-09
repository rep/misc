#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
import subprocess

INT = 'LVDS1'

def xrandr(*args):
	return subprocess.check_output(['xrandr',]+list(args))

def get_connected_screens():
	o = xrandr()
	tmp = filter(lambda x: 'connected' in x, [i.split() for i in o.splitlines()])
	tmp = filter(lambda x: x != INT, [i[0] for i in tmp])
	return tmp

if __name__ == '__main__':
	if len(sys.argv) > 1:
		arg1 = sys.argv[1]
		if arg1 == 'off':
			print 'setting {0} only'.format(INT)
			args = [['--output', i, '--off'] for i in get_connected_screens()]
			xrandr('--output', INT, '--auto', *reduce(lambda x,y: x+y, args,[]))

		elif arg1 == 'left' or arg1 == 'right':
			print 'setting extern {1}-of {0}'.format(INT, arg1)
			args = []
			for e in get_connected_screens():
				args += ['--output', e, '--{0}-of'.format(arg1), INT, '--auto']
			xrandr(*args)
		else:
			print 'command not recognized:', arg1
	else:
		print 'resetting {0} --auto'.format(INT)
		xrandr('--output', INT, '--auto')

