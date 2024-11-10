import sys
import cmd
import os  # Import os to use system-specific clear commands

# Allow import of modules from both Linux and Windows directories
sys.path.append('linux')
sys.path.append('windows')

# Import platform-specific modules
if sys.platform == 'linux':
    from linux.network_con import ping_test, dns_lookup, trace_route
    from linux.speedtest import speed_test
    from linux.network_interface import network_interfaces_info
    from linux.wifianalysis import get_wireless_interface, get_iw_info, get_wifi_signal_strength, get_wifi_info
    from linux.portscan import port_scan
    from linux.security import NetworkSecurityCheck
    from linux.logs_reporting import run
elif sys.platform == 'win32':
    from windows.network_con import ping_test, dns_lookup, trace_route
    from windows.speedtest import speed_test
    from windows.network_interface import network_interfaces_info
    from windows.wifianalysis import get_wireless_interface, get_iw_info, get_wifi_signal_strength, get_wifi_info_nmcli
    from windows.portscan import port_scan
    from windows.security import NetworkSecurityCheck

class NetworkDiagnose(cmd.Cmd):
    prompt = "NetDiagnose>>>"
    intro =r"""                 _   _          _     _____    _                                              
                | \ | |        | |   |  __ \  (_)                                              
                |  \| |   ___  | |_  | |  | |  _    __ _    __ _   _ __     ___    ___    ___  
                | . ` |  / _ \ | __| | |  | | | |  / _` |  / _` | | '_ \   / _ \  / __|  / _ \ 
                | |\  | |  __/ | |_  | |__| | | | | (_| | | (_| | | | | | | (_) | \__ \ |  __/ 
                |_| \_|  \___|  \__| |_____/  |_|  \__,_|  \__, | |_| |_|  \___/  |___/  \___| 
                                                            __/ |                              
                                                           |___/                               
Welcome to the Network Diagnostic Tool. Enter 'diagnose' to see options or 'help' for assistance."""
    
    def do_diagnose(self, arg):
        print("\nChoose an option:\n"
              "1. Network Information\n"
              "2. Speed Test\n"
              "3. Network Interface\n"
              "4. Wi-Fi Analysis\n"
              "5. Port Scan\n"
              "6. Security Information\n"
              "7. Report Full Test Log\n"
              "8. Terminal\n"
        )
        option = input("Enter Option: ")
        if option == '1':
            self.network_information()
        elif option == '2':
            self.run_speed_test()
        elif option == '3':
            self.show_network_interfaces()
        elif option == '4':
            self.wifi_analysis()
        elif option == '5':
            self.run_port_scan()
        elif option == '6':
            self.security_check()
        elif option == '7':
            run()
        elif option == '8':
            pass
        else:
            print("Invalid Option")

    def network_information(self):
        input_ip = input("Enter IP (default: 8.8.8.8): ") or "8.8.8.8"
        input_dns = input("Enter DNS (default: www.google.com): ") or "www.google.com"
        input_route = input("Enter Route (default: 8.8.8.8): ") or "8.8.8.8"

        print(ping_test(input_ip))
        print(dns_lookup(input_dns))
        print(trace_route(input_route))

    def run_speed_test(self):
        print(speed_test())

    def show_network_interfaces(self):
        network_interfaces_info()

    def wifi_analysis(self):
        print(get_iw_info())
        print(get_wireless_interface())
        print(get_wifi_signal_strength())
        print(get_wifi_info())

    def run_port_scan(self):
        port_scan()

    def security_check(self):
        target_ip = input("Enter Target IP (default: 8.8.8.8): ") or "8.8.8.8"
        port = input("Enter Port (default: 300): ") or "300"
        hostname = input("Enter Hostname (default: www.google.com): ") or "www.google.com"

        print(NetworkSecurityCheck.nmap_scan(target_ip, int(port)))
        print(NetworkSecurityCheck.firewall_detection(target_ip, int(port)))
        print(NetworkSecurityCheck.ssl_tls_inspection(hostname))

    def do_clear(self, arg):
        """Clear the console screen."""
        os.system('cls' if sys.platform == 'win32' else 'clear')

    def do_exit(self, arg):
        print("Exiting...")
        return True

    def do_help(self, arg):
        print("\nAvailable commands:\n"
              "diagnose - Run network diagnostics\n"
              "clear    - Clear the console screen\n"
              "help     - Show this help message\n"
              "exit     - Exit the tool\n")
   
    def default(self, line):
        print(f"Unknown command: {line}. Type 'help' for available commands.")


def main():
    NetworkDiagnose().cmdloop()


if __name__ == "__main__":
    main()
