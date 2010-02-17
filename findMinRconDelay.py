#!/usr/bin/env python


import time
import traceback
import sys 
from pyquake3 import Connection
from pyquake3 import ConnectionError

def findMinimalTimout(ip, port, rconpasswd, delay=1000):

	
	sys.stdout.write("assessing minimal timeout for rcon commands")
	
	rconcommand = "mapname"
	nbOfTests = 10
	
	try:
		for ms in range(delay, 10, -10):
			sec = (ms * 1.0) / 1000
			sys.stdout.write("\ntrying with %.3f: " % sec)
			failcount = 0
			for i in range(nbOfTests):
				try:
					c = Connection(ip, port, timeout=sec, retries=1 )
					c.command("rcon \"%s\" %s" % (rconpasswd, rconcommand))
					c.close()
					sys.stdout.write('.')					
				except ConnectionError:
					c.close()
					sys.stdout.write('F') 
					failcount += 1
					if failcount >= (nbOfTests / 2):
						sys.stdout.write("\n\ntimeout must be higher than %s sec\n" % sec)
						sys.exit(0)
				sys.stdout.flush()
	except SystemExit:
		pass
	except:
		traceback.print_exc()
	
	
	
if __name__ == '__main__':

	if len(sys.argv) < 5:
		print "Usage: %s <ip> <port> <rconpass> <delay in ms>" % sys.argv[0]
	else:
		findMinimalTimout(sys.argv[1], int(sys.argv[2]), sys.argv[3], delay=int(sys.argv[4]))
		