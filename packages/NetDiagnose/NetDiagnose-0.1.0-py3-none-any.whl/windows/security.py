import socket
import ssl
import subprocess


class NetworkSecurityCheck:
    @staticmethod
    def install_nmap():
        """
        Installs nmap using Chocolatey if it is not installed.
        Only works if Chocolatey is installed on the system.
        """
        try:
            # Check if nmap is already installed
            result = subprocess.run(["nmap", "--version"], capture_output=True, text=True)
            if "Nmap version" in result.stdout:
                print("nmap is already installed.")
                return

            # Attempt to install nmap using Chocolatey
            print("nmap is not installed. Attempting installation with Chocolatey...")
            choco_install = subprocess.run(["choco", "install", "nmap", "-y"], capture_output=True, text=True)
            if choco_install.returncode == 0:
                print("nmap installed successfully.")
            else:
                print("Failed to install nmap. Ensure Chocolatey is installed and try again.")
        except FileNotFoundError:
            print("Chocolatey is not installed. Please install Chocolatey to use automatic nmap installation.")
        except Exception as e:
            print(f"Error installing nmap: {e}")

    @staticmethod
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
            # Check if nmap is installed
            result = subprocess.run(["nmap", "-Pn", "-p", str(port), target_ip], capture_output=True, text=True)
            print(result.stdout)
        except FileNotFoundError:
            print("nmap is not installed. Attempting to install nmap...")
            NetworkSecurityCheck.install_nmap()
            # Try running nmap again after installation
            try:
                result = subprocess.run(["nmap", "-Pn", "-p", str(port), target_ip], capture_output=True, text=True)
                print(result.stdout)
            except Exception as e:
                print(f"Error running nmap after installation attempt: {e}")
        except Exception as e:
            print(f"Error running nmap: {e}")

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

                    # Check for hostname validity manually
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

        print(result)
