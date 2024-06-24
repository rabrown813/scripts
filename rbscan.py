#!/usr/bin/env python

import argparse
import scapy.all as scapy

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="IP range to scan")
    options = parser.parse_args()
    return options
def scan(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_bc = broadcast / arp_req
    reply_list = scapy.srp(arp_req_bc, timeout=2, verbose=False)[0]
    #    print(reply_list)

    clients_info = []
    for i in reply_list:
        client_key = {"ip": i[1].psrc, "mac": i[1].hwsrc}
        clients_info.append(client_key)
    return clients_info


def print_results(result_list):
    print("IP\t\t\tMAC Address\n- - - - - - - - - - - - - - - - - - - - - ")
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])

options = get_arguments()
scan_result = scan(options.target)
print_results(scan_result)


