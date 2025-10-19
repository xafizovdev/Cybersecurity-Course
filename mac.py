import subprocess
import optparse
import re
def get_args():
    parser=optparse.OptionParser()
    parser.add_option("-i","--interface",dest="interface",help="Interface to change its MAC adress")
    parser.add_option("-m","--mac",dest="mac_adress",help=" MAC adress")
    options,args=parser.parse_args()
    if not options.interface:
        parser.error("Please identify an interface , use --help for more information")
    elif not options.mac_adress:
        parser.error("Please identify a MAC adress , use --help for more information")
    return options


def mac_changer(interface,mac_adress):
    print("[+] Changing MAC adrres for "+interface+ " to " + mac_adress)

    subprocess.call(["ifconfig",interface,"down"])
    subprocess.call(["ifconfig",interface,"hw","ether",mac_adress])
    subprocess.call(["ifconfig",interface,"up"])

def get_mac_result(interface):

    ifconfig_result=subprocess.check_output(["ifconfig" , interface]).decode()

    pattern=r'\b([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b'

    match=re.search(pattern,ifconfig_result)
    if match:
        return match.group()
    else:
        print("[-] Could not find the MAC")

options=get_args()

current_mac=get_mac_result(options.interface)
print("Current MAC : " + str(current_mac))

mac_changer(options.interface,options.mac_adress)


current_mac=get_mac_result(options.interface)

if current_mac == options.mac_adress:
    print("[+] MAC adress was successfully changed to : "+ current_mac)
else:
    print("[-] MAC adress did not get change .")
