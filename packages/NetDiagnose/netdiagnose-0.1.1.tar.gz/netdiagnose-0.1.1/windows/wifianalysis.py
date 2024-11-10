import psutil
import subprocess

def get_wireless_interface():
    interfaces = psutil.net_if_addrs()
    for interface_name in interfaces:
        if 'wlan' in interface_name or 'wifi' in interface_name or 'wl' in interface_name:
            return interface_name
    return None

# Function to retrieve Wi-Fi interface details using netsh (Windows)
def get_iw_info():
    interface = get_wireless_interface()
    if not interface:
        print("No wireless interface found.")
        return
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], universal_newlines=True)
        print("Wi-Fi Interface Info:")
        print(result)
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving Wi-Fi interface info: {e}")

# Function to retrieve signal strength and link quality using netsh (Windows)
def get_wifi_signal_strength():
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], universal_newlines=True)
        print("Wi-Fi Signal Strength:")
        for line in result.splitlines():
            if "Signal" in line:
                print(f"  {line.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving Wi-Fi signal strength: {e}")

# Function to retrieve Wi-Fi info using netsh (Windows)
def get_wifi_info():
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"], universal_newlines=True)
        print("Available Wi-Fi Networks:")
        for line in result.splitlines():
            if "SSID" in line or "Signal" in line or "Authentication" in line:
                if "Authentication" in line and "Open" in line:
                    security = "None"
                else:
                    security = line.split(":")[1].strip()
                print(f"  {line.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving Wi-Fi info: {e}")
