import psutil
import subprocess


def get_wireless_interface():
    interfaces = psutil.net_if_addrs()
    for interface_name in interfaces:
        if 'wlan' in interface_name or 'wifi' in interface_name or 'wl' in interface_name:
            return interface_name
    return None

# Function to retrieve Wi-Fi interface details using iw
def get_iw_info():
    interface = get_wireless_interface()
    if not interface:
        return("No wireless interface found.")
    try:
        result = subprocess.check_output(["iw", "dev", interface, "info"], universal_newlines=True)
        print("Wi-Fi Interface Info (via iw):")
        return(result)
    except subprocess.CalledProcessError as e:
        return(f"Error retrieving Wi-Fi interface info via iw: {e}")

# Function to retrieve signal strength and link quality using iwconfig
def get_wifi_signal_strength():
    try:
        result = subprocess.check_output(["iwconfig"], universal_newlines=True)
        print("Wi-Fi Signal Strength (via iwconfig):")
        for line in result.splitlines():
            if "Link Quality" in line:
                return(f"  {line.strip()}")
    except subprocess.CalledProcessError as e:
        return(f"Error retrieving Wi-Fi signal strength via iwconfig: {e}")

# Function to retrieve Wi-Fi info using nmcli
def get_wifi_info():
    try:
        result = subprocess.check_output(["nmcli", "-t", "-f", "SSID,SIGNAL,SECURITY,CHAN", "device", "wifi", "list"], universal_newlines=True)
        print("Available Wi-Fi Networks (via nmcli):")
        channels = {}
        for line in result.splitlines():
            ssid, signal, security, channel = line.split(":")
            if not security:
                security = "None"
            print(f"SSID: {ssid}, Signal Strength: {signal}%, Security: {security}, Channel: {channel}")
            if channel in channels:
                channels[channel] += 1
            else:
                channels[channel] = 1
        print("\nChannel Interference:")
        for channel, count in channels.items():
            return(f"Channel {channel}: {count} networks")
    except subprocess.CalledProcessError as e:
        return(f"Error retrieving Wi-Fi info via nmcli: {e}")




