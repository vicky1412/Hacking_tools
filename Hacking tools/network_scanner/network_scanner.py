import scapy.all as scapy
import argparse

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help= "Target ip/ip range")
    options = parser.parse_args()
    if not options.target:
        parser.error("[-]Enter a valid ip/range")
    return options

def scan(ip):
    arp_reques = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    broadcast_arp_request = broadcast/arp_reques
    answered = scapy.srp(broadcast_arp_request,timeout=1,verbose=False)[0]


    client_list = []
    for element in answered:
        client_dist = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        client_list.append(client_dist)
    return client_list

def print_list(result_list):
    print("____________________________________________\nip\t\t\tmac address\n---------------------------------------------")
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])


option = arg_parse()
scan_result = scan(option.target)
print_list(scan_result)