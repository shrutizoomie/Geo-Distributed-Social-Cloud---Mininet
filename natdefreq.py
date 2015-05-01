"""
Example to create a Mininet topology and connect it to the internet via NAT
through eth0 on the host.

Glen Gibb, February 2011

(slight modifications by BL, 5/13)
"""
import re
import os, sys
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import lg
from mininet.node import Node
from mininet.topolib import TreeNet
from mininet.node import Controller, OVSSwitch
from mininet.util import dumpNodeConnections
from mininet.link import TCLink
from mininet.log import setLogLevel

from time import time
from select import poll, POLLIN
from subprocess import Popen, PIPE

#################################

def startNAT( root, inetIntf='eth0', subnet='10.0/8' ):
    """Start NAT/forwarding between Mininet and external network
    root: node to access iptables from
    inetIntf: interface for internet access
    subnet: Mininet subnet (default 10.0/8)="""

    # Identify the interface connecting to the mininet network
    localIntf =  root.defaultIntf()

    # Flush any currently active rules
    root.cmd( 'iptables -F' )
    root.cmd( 'iptables -t nat -F' )

    # Create default entries for unmatched traffic
    root.cmd( 'iptables -P INPUT ACCEPT' )
    root.cmd( 'iptables -P OUTPUT ACCEPT' )
    root.cmd( 'iptables -P FORWARD DROP' )

    # Configure NAT
    root.cmd( 'iptables -I FORWARD -i', localIntf, '-d', subnet, '-j DROP' )
    root.cmd( 'iptables -A FORWARD -i', localIntf, '-s', subnet, '-j ACCEPT' )
    root.cmd( 'iptables -A FORWARD -i', inetIntf, '-d', subnet, '-j ACCEPT' )
    root.cmd( 'iptables -t nat -A POSTROUTING -o ', inetIntf, '-j MASQUERADE' )

    # Instruct the kernel to perform forwarding
    root.cmd( 'sysctl net.ipv4.ip_forward=1' )

def stopNAT( root ):
    """Stop NAT/forwarding between Mininet and external network"""
    # Flush any currently active rules
    root.cmd( 'iptables -F' )
    root.cmd( 'iptables -t nat -F' )

    # Instruct the kernel to stop forwarding
    root.cmd( 'sysctl net.ipv4.ip_forward=0' )

def fixNetworkManager( root, intf ):
    """Prevent network-manager from messing with our interface,
       by specifying manual configuration in /etc/network/interfaces
       root: a node in the root namespace (for running commands)
       intf: interface name"""
    cfile = '/etc/network/interfaces'
    line = '\niface %s inet manual\n' % intf
    config = open( cfile ).read()
    if line not in config:
        print '*** Adding', line.strip(), 'to', cfile
        with open( cfile, 'a' ) as f:
            f.write( line )
        # Probably need to restart network-manager to be safe -
        # hopefully this won't disconnect you
        root.cmd( 'service network-manager restart' )

def connectToInternet( network, switch='s1', rootip='10.254', subnet='10.0/8'):
    """Connect the network to the internet
       switch: switch to connect to root namespace
       rootip: address for interface in root namespace
       subnet: Mininet subnet"""
    switch = network.get( switch )
    prefixLen = subnet.split( '/' )[ 1 ]

    # Create a node in root namespace
    root = Node( 'root', inNamespace=False )

    # Prevent network-manager from interfering with our interface
    fixNetworkManager( root, 'root-eth0' )

    # Create link between root NS and switch
    link = network.addLink( root, switch )
    link.intf1.setIP( rootip, prefixLen )

    # Start network that now includes link to root namespace
    network.start()

    # Start NAT and establish forwarding
    startNAT( root )

    # Establish routes from end hosts
    for host in network.hosts:
        host.cmd( 'ip route flush root 0/0' )
        host.cmd( 'route add -net', subnet, 'dev', host.defaultIntf() )
        host.cmd( 'route add default gw', rootip )

    return root


########## function of multipoll.py starts ##################

def monitorFiles( outfiles, seconds, timeoutms ):
    "Monitor set of files and return [(host, line)...]"
    devnull = open( '/dev/null', 'a' )
    tails, fdToFile, fdToHost = {}, {}, {}
    for h, outfile in outfiles.iteritems():
        tail = Popen( [ 'tail', '-f', outfile ],
                      stdout=PIPE, stderr=devnull )
        fd = tail.stdout.fileno()
        tails[ h ] = tail
        fdToFile[ fd ] = tail.stdout
        fdToHost[ fd ] = h
    # Prepare to poll output files
    readable = poll()
    for t in tails.values():
        readable.register( t.stdout.fileno(), POLLIN )
    # Run until a set number of seconds have elapsed
    endTime = time() + seconds
    while time() < endTime:
        fdlist = readable.poll(timeoutms)
        if fdlist:
            for fd, _flags in fdlist:
                f = fdToFile[ fd ]
                host = fdToHost[ fd ]
                # Wait for a line of output
                line = f.readline().strip()
                yield host, line
        else:
            # If we timed out, return nothing
            yield None, ''
    for t in tails.values():
        t.terminate()
    devnull.close()  # Not really necessary

########## function of multipoll.py ends ##################


def singleController( reqs ):

    net = Mininet( controller=Controller, switch=OVSSwitch, link=TCLink )

    print "*** Creating the controller***"

    c0 = net.addController( 'c0', port=6633 )

    print "*** Creating switch"
    s1 = net.addSwitch( 's1' )
    s2 = net.addSwitch( 's2' )
    print "*** Creating the hosts"
    hosts1 = [ net.addHost( 'h%d' % n ) for n in 1, 2, 3, 4 ]
    hosts2 = [ net.addHost( 'h%d' % n ) for n in 5, 6, 7, 8 ] 

    print "** creating links"
    for h in hosts1:
	net.addLink( s1, h)

    for h in hosts2:
        net.addLink( s2, h)

    links1 =dict(bw=10, delay='15ms', loss=5, use_htb=True)
    net.addLink( s1, s2, **links1 )
    net.build()
    s1.start( [ c0 ] )
    s2.start( [ c0 ] )

    net.start()

    ############## multi poll integration starts #######################

    hosts = net.hosts     #this creates an array which has list of all the host h1 to h8
    
    server = hosts[ 0 ]   #get the value of first host h1
    
    outfiles, errfiles = {}, {}     #creates two array to store the out files(to show ping outputs)  and err files(to show errprs encountered)

    h1 = net.get('h1')
    
    file = open('/home/mininet/result.txt','w')  #here I am creating one more file to write the request time inn between hosts and cost of streaming
 
    #### Here I am running loop to get each host from hosts array and I am pinging each host from h1 and storing the output in .out file ####### 
    for h in hosts:                       
        outfiles[ h ] = '/home/mininet/%s.out' % h.name
        errfiles[ h ] = '/home/mininet/%s.out' % h.name

        ping_op = h1.cmd('ping -c1', h.IP())   #pinging each host from h1 just for 1 time to get the time value and storing the o/p to ping_op #####         
    	match = re.search('ttl=(\d+) time=([\d.]+)', ping_op)  #extracting time value from output of ping command  #########
    	ttl = match.group(1)
        rtt = match.group(2)  #rtt shows the time in string
        rtt = float(rtt)    #converting string to float
	reqs = float(reqs)
        cost = rtt*reqs      # calculating cost where cost is time* no of reqests. By default I have taken no of req as 10
    	
        #outputting request time and cost in result.txt
        file.write("Request time in between h1 and ") 
        file.write(h.name)
        file.write(" is ")
        file.write(str(rtt))
        file.write("------ and cost of streaming data is ")
        file.write(str(cost))
        file.write("\n")

	#generating traffic by pinging each host from h1 10 times and saving the output to hostname.out file so for h1 the file name will be h1.out
        h.cmdPrint('ping -c10', server.IP(), '>', outfiles[ h ], '2>', errfiles[ h ], '&' )    
    #### For loop Ends ######################################################################
    
    file.close()  #closing result.txt file

    print "Monitoring output for",5, "seconds"

    #for loop for calling monitorFiles fnction 
    for h, line in monitorFiles( outfiles,5, timeoutms=500 ):
        if h:
            print '%s: %s' % ( h.name, line )
    for h in hosts:
        h.cmd('kill %ping')
   
    ################multi[poll ntegration ends ##############################################################i#

    print "dumping host connections"

   

    dumpNodeConnections(net.hosts)
    #net.pingAll()
    rootnode = connectToInternet( net )
    CLI( net )
    net.stop()



if __name__ == '__main__':
    lg.setLogLevel( 'info')
    #singleController()
    reqs = sys.argv[1]
    singleController( reqs )

    #c0 = Controller( 'c0', port=6633 )
    #net = TreeNet( depth=1, fanout=4 )
    #net.addController(c0)
    #net.build()
    #net.start()
    # Configure and start NATted connectivity
    #rootnode = connectToInternet( net )
    print "*** Hosts are running and should have internet connectivity"
    print "*** Type 'exit' or control-D to shut down network"
    #CLI( net )
    # Shut down NAT
    stopNAT( rootnode )
    #net.stop()

