import os, sys
import glob

file_name = sys.argv[1]
hostfile = sys.argv[2]

if hostfile == '1':
	print " Deleting the file under host1"
	print file_name
	os.remove("/home/mininet/projscripts/host1/"+file_name)

if hostfile == '2':
	print "Deleting the file under host2"
	print file_name
	os.remove("/home/mininet/projscripts/host2/"+file_name)

if hostfile == '3':
	print "Deleting the file under host3"
	print file_name
	os.remove("/home/mininet/projscripts/host3/"+file_name)

if hostfile == '4':
	print "Deleting the file under host4"
	print file_name
	os.remove("/home/mininet/projscripts/host4/"+file_name)

		




