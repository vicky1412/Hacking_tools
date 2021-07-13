import scapy.all as scapy
import argparse


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help= "specify the interface")
    options = parser.parse_args()
    if not options.interface:
        parser.error("[-]Enter an interface to check")
    return options


def sniff(interface):
    scapy.sniff(iface=interface,store=False,prn=process_packet)

def get_mac(ip):
    arp_reques = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    broadcast_arp_request = broadcast/arp_reques
    answered = scapy.srp(broadcast_arp_request,timeout=1,verbose=False)[0]

    return answered[0][1].hwsrc


def process_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op==2:
        print("arp response")
        response_mac = packet[scapy.ARP].hwsrc
        real_mac = get_mac(packet[scapy.ARP].psrc )
        if response_mac != real_mac:
            print("Attack detected")



option = arg_parse()
sniff(option.interface)