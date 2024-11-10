import psutil

def port_scan():
    # Dictionary to store port usage information
    port_usage = {}

    # Get all network connections
    connections = psutil.net_connections()

    for conn in connections:
        laddr = conn.laddr
        if laddr:
            port = laddr.port
            pid = conn.pid
            if pid:
                try:
                    process = psutil.Process(pid)
                    app_name = process.name()
                except psutil.NoSuchProcess:
                    app_name = "Unknown"
            else:
                app_name = "Unknown"
            port_usage[port] = app_name

    # Print used ports and their applications
    print("Used Ports and Applications:")
    for port, app in sorted(port_usage.items()):
        print(f"Port {port}: {app}")

    # Find and print ranges of free ports (assuming ports 1-65535)
    print("\nFree Port Ranges:")
    used_ports = sorted(port_usage.keys())
    free_ranges = []
    start = 1

    for port in used_ports:
        if port > start:
            free_ranges.append((start, port - 1))
        start = port + 1

    if start <= 65535:
        free_ranges.append((start, 65535))

    for start, end in free_ranges:
        if start == end:
            print(f"Port {start} is free")
        else:
            print(f"Ports {start}-{end} are free")
