from mininet.net import Mininet
from mininet.node import Node
from mininet.link import TCLink
from mininet.log import  setLogLevel, info
from threading import Timer
from mininet.util import quietRun
from time import sleep
from mininet.cli import CLI


def myNet(cname='controller', cargs='-v ptcp:'):
    "Create network from scratch using Open vSwitch."
    info( "*** Creating nodes\n" )
    controller = Node( 'c0', inNamespace=False )
    s1 = Node( 's1', inNamespace=False )
    s2 = Node( 's2', inNamespace=False )
    s3 = Node( 's3', inNamespace=False )
    s4 = Node( 's4', inNamespace=False )
    s6 = Node( 's6', inNamespace=False )
    s7 = Node( 's7', inNamespace=False )
    h1 = Node( 'h1' )
    h2 = Node( 'h2' )
    h3 = Node( 'h3' )
    h4 = Node( 'h4' )
    h5 = Node( 'h5' )
    h6 = Node( 'h6' )
    h7 = Node( 'h7' )
    h8 = Node( 'h8' )
    server = Node( 'server' )

    info( "*** Creating links\n" )
    linkopts0=dict(bw=10, delay='1ms', loss=0)
    TCLink( s1, s2, **linkopts0)
    TCLink( s2, s3, **linkopts0)
    TCLink( s2, s4, **linkopts0)
    TCLink( s2, s6, **linkopts0)
    TCLink( s2, s7, **linkopts0)
    TCLink( s1, h3, **linkopts0)
    TCLink( s1, h4, **linkopts0)
    TCLink( s3, h1, **linkopts0)
    TCLink( s4, h7, **linkopts0)
    TCLink( s4, h8, **linkopts0)
    TCLink( s6, h5, **linkopts0)
    TCLink( s6, h6, **linkopts0)
    TCLink( s7, server, **linkopts0)
    


    info( "*** Configuring hosts\n" )
    h1.setIP( '30.30.1.20/22' )
    h2.setIP( '30.30.1.21/22' )
    h3.setIP( '30.30.1.22/22' )
    h4.setIP( '30.30.1.23/22' )
    h5.setIP( '30.30.1.24/22' )
    h6.setIP( '30.30.1.25/22' )
    h7.setIP( '30.30.1.26/22' )
    h8.setIP( '30.30.1.27/22' )
    server.setIP( '30.30.1.28/22' )
    h1.setMAC('00:00:00:43:92:01')
    h2.setMAC('00:00:00:43:92:02')
    h3.setMAC('00:00:00:43:92:03')
    h4.setMAC('00:00:00:43:92:04')
    h5.setMAC('00:00:00:43:92:05')
    h6.setMAC('00:00:00:43:92:06')
    h7.setMAC('00:00:00:43:92:07')
    h8.setMAC('00:00:00:43:92:08')
    server.setMAC('00:00:00:43:92:09')
    s1.setMAC('00:00:02:43:92:01')
    s2.setMAC('00:00:02:43:92:02')
    s3.setMAC('00:00:02:43:92:03')
    s4.setMAC('00:00:02:43:92:04')
    s6.setMAC('00:00:02:43:92:05')
    s7.setMAC('00:00:02:43:92:06')
               

    info( "*** Starting network using Open vSwitch\n" )

    s1.cmd( 'ovs-vsctl del-br dp1' )
    s1.cmd( 'ovs-vsctl add-br dp1' )
    s2.cmd( 'ovs-vsctl del-br dp2' )
    s2.cmd( 'ovs-vsctl add-br dp2' )
    s3.cmd( 'ovs-vsctl del-br dp3' )
    s3.cmd( 'ovs-vsctl add-br dp3' )
    s4.cmd( 'ovs-vsctl del-br dp4' )
    s4.cmd( 'ovs-vsctl add-br dp4' )
    s6.cmd( 'ovs-vsctl del-br dp6' )
    s6.cmd( 'ovs-vsctl add-br dp6' )
    s7.cmd( 'ovs-vsctl del-br dp7' )
    s7.cmd( 'ovs-vsctl add-br dp7' )
 

    controller.cmd( cname + ' ' + cargs + '&' )          
    for intf in s1.intfs.values():
        print intf
        print s1.cmd( 'ovs-vsctl add-port dp1 %s' % intf )

    for intf in s2.intfs.values():
        print intf
        print s2.cmd( 'ovs-vsctl add-port dp2 %s' % intf )

    for intf in s3.intfs.values():
        print intf
        print s3.cmd( 'ovs-vsctl add-port dp3 %s' % intf )

    for intf in s4.intfs.values():
        print intf
        print s4.cmd( 'ovs-vsctl add-port dp4 %s' % intf )

    for intf in s6.intfs.values():
        print intf
        print s6.cmd( 'ovs-vsctl add-port dp6 %s' % intf )

    for intf in s7.intfs.values():
        print intf
        print s7.cmd( 'ovs-vsctl add-port dp7 %s' % intf )

    # Note: controller and switch are in root namespace, and we
    # can connect via loopback interface
    s1.cmd( 'ovs-vsctl set-controller dp0 tcp:127.0.0.1:6633' )
    s2.cmd( 'ovs-vsctl set-controller dp0 tcp:127.0.0.1:6633' )
    s3.cmd( 'ovs-vsctl set-controller dp0 tcp:127.0.0.1:6633' )
    s4.cmd( 'ovs-vsctl set-controller dp0 tcp:127.0.0.1:6633' )
    s6.cmd( 'ovs-vsctl set-controller dp0 tcp:127.0.0.1:6633' )
    s7.cmd( 'ovs-vsctl set-controller dp0 tcp:127.0.0.1:6633' )
   

    info( '*** Waiting for switch to connect to controller' )
    while 'is_connected' not in quietRun( 'ovs-vsctl show' ):
        sleep( 1 )
        info( '.' )
    info( '\n' )

    #print s0.cmd('ovs-ofctl show dp0')
    #info( "*** Running test\n" )
    h3.cmdPrint( 'ping -c 3 ' + h2.IP() )
    h4.cmdPrint( 'ping -c 3 ' + h2.IP() )
    h2.cmd('iperf -s &')
    h3.cmdPrint('iperf -c 30.30.1.23 -t 10')
    h4.cmdPrint('iperf -c 30.30.1.23 -t 10')
    s1.cmdPrint('ethtool -K s0-eth2 gro off')
    s1.cmdPrint('tc qdisc del dev s0-eth2 root')
    s1.cmdPrint('tc qdisc add dev s0-eth2 root handle 1: cbq avpkt 1000 bandwidth 10Mbit rate 512kbit bounded isolated')
    h3.cmdPrint('iperf -c 30.30.1.23 -t 10')
    h4.cmdPrint('iperf -c 30.30.1.23 -t 10')

 
    info( "*** Stopping network\n" )
    controller.cmd( 'kill %' + cname )
    s1.cmd( 'ovs-vsctl del-br dp1' )
    s1.deleteIntfs()
    s2.cmd( 'ovs-vsctl del-br dp2' )
    s2.deleteIntfs()
    info( '\n' )

 

if __name__ == '__main__':
    global net
    setLogLevel( 'info' )
    info( '*** Scratch network demo (kernel datapath)\n' )
    Mininet.init()
    myNet()