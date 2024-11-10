import psutil
import socket


def network_interfaces_info():
    # Retrieve network interface details
    interfaces = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    
    for interface_name, addresses in interfaces.items():
        print(f"\nInterface: {interface_name}")
        
        # Display interface stats (is it up, duplex, speed, MTU)
        if interface_name in stats:
            iface_stats = stats[interface_name]
            print(f"  Interface: {interface_name}")
            print(f"  Status: {'Up' if iface_stats.isup else 'Down'}")
            print(f"  Duplex: {iface_stats.duplex}")
            print(f"  Speed: {iface_stats.speed} Mbps")
            print(f"  MTU: {iface_stats.mtu}")
        
        # Display IP addresses and MAC address
        for address in addresses:
            if address.family == socket.AF_NETLINK:
                
                print(f"  MAC Address: {address.address}")
            elif address.family == socket.AF_INET:
                print(f"  IPv4 Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast IP: {address.broadcast}")
            elif address.family == socket.AF_INET6:
                print(f"  IPv6 Address: {address.address}")
                print(f"  Netmask: {address.netmask}")