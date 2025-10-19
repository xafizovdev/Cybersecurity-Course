import scapy.all as scapy
import optparse

def arg():
    parser=optparse.OptionParser()
    parser.add_option("-i","--iq",dest="ip",help="IP adress to search")
    options,args=parser.parse_args()
    if not options.ip:
        parser.error("Please identify an ip adress , use --help for more information")
    return options


def scan(ip):
    arp_request=scapy.ARP(pdst=ip)
    
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    
    arp_broadcast=broadcast/arp_request
    answered=scapy.srp(arp_broadcast, timeout=2,verbose=False)[0]
    client_list=[]
    for a in answered:
        client_dict={
            "ip":a[1].psrc,
            "mac_adress":a[1].hwsrc
        }
        client_list.append(client_dict)
    return client_list
 
def result(answer_list):
    print("IP\t\t\tMAC Adress\n -------------------------")
    for client in answer_list:
        print(client["ip"] + "\t\t" + client["mac_adress"])

options=arg()


r=scan(options.ip)
result(r)

