import os, sys

print "Host1 has the files:"
for file in os.listdir("/home/mininet/mininet/projScripts/host1"):
	if file.endswith(".pdf") or file.endswith(".txt") or file.endswith(".mp3"):
		st=os.stat("/home/mininet/mininet/projScripts/host1/"+file)
		atime=st.st_atime
		print file
		print atime
print "Host2 has the files:"
for file in os.listdir("/home/mininet/mininet/projScripts/host2"):
        if file.endswith(".pdf") or file.endswith(".txt") or file.endswith(".mp3"):
                st=os.stat("/home/mininet/mininet/projScripts/host2/"+file)
                atime=st.st_atime
                print file
                print atime
print "Host3 has the files:"
for file in os.listdir("/home/mininet/mininet/projScripts/host3"):
        if file.endswith(".pdf") or file.endswith(".txt") or file.endswith(".mp3"):
                st=os.stat("/home/mininet/mininet/projScripts/host3/"+file)
                atime=st.st_atime
                print file
                print atime
print "Host4 has the files:"
for file in os.listdir("/home/mininet/mininet/projScripts/host4"):
        if file.endswith(".pdf") or file.endswith(".txt") or file.endswith(".mp3"):
                st=os.stat("/home/mininet/mininet/projScripts/host4/"+file)
                atime=st.st_atime
                print file
                print atime
print "Host5 has the files:"
for file in os.listdir("/home/mininet/mininet/projScripts/host5"):
        if file.endswith(".pdf") or file.endswith(".txt") or file.endswith(".mp3"):
                st=os.stat("/home/mininet/mininet/projScripts/host5/"+file)
                atime=st.st_atime
                print file
                print atime
print "Host6 has the files:"
for file in os.listdir("/home/mininet/mininet/projScripts/host6"):
        if file.endswith(".pdf") or file.endswith(".txt") or file.endswith(".mp3"):
                st=os.stat("/home/mininet/mininet/projScripts/host6/"+file)
                atime=st.st_atime
                print file
                print atime
print "Host7 has the files:"
for file in os.listdir("/home/mininet/mininet/projScripts/host7"):
        if file.endswith(".pdf") or file.endswith(".txt") or file.endswith(".mp3"):
                st=os.stat("/home/mininet/mininet/projScripts/host7/"+file)
                atime=st.st_atime
                print file
                print atime
print "Host8 has the files:"
for file in os.listdir("/home/mininet/mininet/projScripts/host8"):
        if file.endswith(".pdf") or file.endswith(".txt") or file.endswith(".mp3"):
                st=os.stat("/home/mininet/mininet/projScripts/host8/"+file)
                atime=st.st_atime
                print file
                print atime



