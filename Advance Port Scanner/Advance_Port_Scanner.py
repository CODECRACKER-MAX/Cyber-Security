import argparse
import sys
from scapy.all import *


def design():
    print("""
  ____            _     ____                                  
 |  _ \ ___  _ __| |_  / ___|  ___ __ _ _ __  _ __   ___ _ __ 
 | |_) / _ \| '__| __| \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
  |  __/ (_) | |  | |_   ___) | (_| (_| | | | | | | |  __/ |   
 |_|   \___/|_|   \__| |____/ \___\__,_|_| |_|_| |_|\___|_|      
                                                                by barun

""")


# Function to perform TCP connect scan
def tcp_connect_scan(target, port):
    response = sr1(IP(dst=target) / TCP(dport=port, flags="S"), timeout=2, verbose=False)
    if response is not None and response.haslayer(TCP):
        if response.getlayer(TCP).flags == 0x12:
            send(IP(dst=target) / TCP(dport=port, flags="R"), verbose=False)
            return "Open"
        elif response.getlayer(TCP).flags == 0x14:
            return "Closed"
    return "Unknown"


# Function to perform TCP SYN (stealth) scan
def tcp_syn_scan(target, port):
    response = sr1(IP(dst=target) / TCP(dport=port, flags="S"), timeout=2, verbose=False)
    if response is not None and response.haslayer(TCP):
        if response.getlayer(TCP).flags == 0x12:
            send(IP(dst=target) / TCP(dport=port, flags="R"), verbose=False)
            return "Open"
        elif response.getlayer(TCP).flags == 0x14:
            return "Closed"
    return "Unknown"


# Function to perform TCP FIN scan
def tcp_fin_scan(target, port):
    response = sr1(IP(dst=target) / TCP(dport=port, flags="F"), timeout=2, verbose=False)
    if response is not None and response.haslayer(TCP):
        if response.getlayer(TCP).flags == 0x14:
            return "Closed"
        elif response.getlayer(TCP).flags == 0x04:
            return "Open"
    return "Unknown"


# Function to perform TCP Xmas scan
def tcp_xmas_scan(target, port):
    response = sr1(IP(dst=target) / TCP(dport=port, flags="FPU"), timeout=2, verbose=False)
    if response is not None and response.haslayer(TCP):
        if response.getlayer(TCP).flags == 0x14:
            return "Closed"
        elif response.getlayer(TCP).flags == 0x04:
            return "Open"
    return "Unknown"


# Function to perform TCP Null scan
def tcp_null_scan(target, port):
    response = sr1(IP(dst=target) / TCP(dport=port, flags=""), timeout=2, verbose=False)
    if response is not None and response.haslayer(TCP):
        if response.getlayer(TCP).flags == 0x14:
            return "Closed"
        elif response.getlayer(TCP).flags == 0x04:
            return "Open"
    return "Unknown"


# Function to perform UDP scan
def udp_scan(target, port):
    response = sr1(IP(dst=target) / UDP(dport=port), timeout=5, verbose=False)
    if response is not None and response.haslayer(UDP):
        return "Open"
    elif response is not None and response.haslayer(ICMP):
        if int(response.getlayer(ICMP).type) == 3 and int(response.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]:
            return "Closed"
    return "Unknown"


# Function to perform ACK scan
def ack_scan(target, port):
    response = sr1(IP(dst=target) / TCP(dport=port, flags="A"), timeout=2, verbose=False)
    if response is not None and response.haslayer(TCP):
        if response.getlayer(TCP).flags == 0x4:
            return "Unfiltered"
    return "Filtered"


# Parse port ranges from string argument
def parse_ports(port_arg):
    ports = []
    port_ranges = port_arg.split(',')
    for port_range in port_ranges:
        if '-' in port_range:
            start, end = map(int, port_range.split('-'))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(port_range))
    return ports


# Parse scan type argument
def parse_scan_type(scan_type_arg):
    scan_types = {
        'T': tcp_connect_scan,
        'S': tcp_syn_scan,
        'F': tcp_fin_scan,
        'X': tcp_xmas_scan,
        'N': tcp_null_scan,
        'U': udp_scan,
        'A': ack_scan,
    }
    return scan_types.get(scan_type_arg)


design()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Port Scanner')
    parser.add_argument('-IP', metavar='ip', type=str, help='Target IP Address', required=True)
    parser.add_argument('-p', metavar='ports', type=str, help='Port(s) to scan, separated by commas', required=True)
    parser.add_argument('-s', metavar='scan_type', type=str, choices=['T', 'S', 'F', 'X', 'N', 'U', 'A'],
                        help='Scan type', required=True)
    args = parser.parse_args()

    target = args.IP
    ports = parse_ports(args.p)
    scan_function = parse_scan_type(args.s)

    if scan_function:
        print(f"Running {str(parse_scan_type(args.s))} scan:")

        for port in ports:
            print(f"Port {port}: {scan_function(target, port)}")
    else:
        print("Invalid scan type specified.")
