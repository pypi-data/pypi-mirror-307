import socket
import ssl
import subprocess
from scapy.all import IP, TCP, sr1

from linux.portscan import port_scan;


class NetworkSecurityCheck:
    def nmap_scan(target_ip, port):
        """
        Runs an nmap scan on the target IP and port if nmap is installed.

        Args:
            target_ip (str): The IP address of the target.
            port (int): Port number to scan.

        Returns:
            str: nmap scan result.
        """

        port = int(port)
        try:
            result = subprocess.run(["nmap", "-Pn", "-p", str(port), target_ip], capture_output=True, text=True)
            return(result.stdout)
        except FileNotFoundError:
            return("nmap is not installed on this system.")
        except Exception as e:
            return(f"Error running nmap: {e}")

    @staticmethod
    def firewall_detection(target_ip, port):
        """
        Checks if there is a firewall blocking certain ports on the target IP.

        Args:
            target_ip (str): The IP address of the target.
            port (int): Port number to check.

        Returns:
            str: Result of the firewall check.
        """
        port = int(port)
        try:
            packet = IP(dst=target_ip) / TCP(dport=port, flags='S')
            response = sr1(packet, timeout=2, verbose=0)

            if response is None:
                return(f"Port {port} seems filtered or blocked by a firewall.")
            elif response.haslayer(TCP):
                if response.getlayer(TCP).flags == 0x12:  # SYN-ACK response
                    return(f"Port {port} is open and reachable.")
                elif response.getlayer(TCP).flags == 0x14:  # RST response
                    return(f"Port {port} is closed but not filtered by a firewall.")
            else:    
             return(f"Unexpected response on port {port}.")
        except PermissionError:
            return("Firewall detection requires elevated permissions (e.g., run as root).")
        except Exception as e:
            return(f"Error in firewall detection: {e}")

    @staticmethod
    def ssl_tls_inspection(hostname, port=443):
        """
        Inspects SSL/TLS certificate and configuration for potential vulnerabilities.

        Args:
            hostname (str): The hostname of the target server.
            port (int): Port to connect, typically 443 for HTTPS.

        Returns:
            dict: SSL/TLS details or errors.
        """
        result = {
            "hostname": hostname,
            "ssl_version": None,
            "certificate_valid": False,
            "issuer": None,
            "expiry_date": None,
            "error": None
        }

        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    result["ssl_version"] = ssock.version()

                    # Check for hostname validity manually (if ssl.match_hostname is unavailable)
                    common_names = [entry[1] for entry in cert.get('subject', []) if entry[0] == 'commonName']
                    subject_alt_names = [san[1] for san in cert.get('subjectAltName', [])]

                    if hostname in common_names or hostname in subject_alt_names:
                        result["certificate_valid"] = True
                    result["issuer"] = cert.get("issuer")
                    result["expiry_date"] = cert.get("notAfter")
        except ssl.SSLCertVerificationError as e:
            result["error"] = f"SSL Certificate Verification Error: {e}"
        except Exception as e:
            result["error"] = f"Unexpected error: {e}"



            
        return(result)