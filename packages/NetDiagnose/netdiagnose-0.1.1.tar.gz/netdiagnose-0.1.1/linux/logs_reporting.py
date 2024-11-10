import sys
import os
from email.message import EmailMessage
import smtplib
from email.utils import formataddr

# Allow import of modules from both Linux and Windows directories
sys.path.append('linux')
sys.path.append('windows')

# Import platform-specific modules
if sys.platform == 'linux':
    from linux.network_con import ping_test, dns_lookup, trace_route
    from linux.speedtest import speed_test
    from linux.wifianalysis import get_wireless_interface, get_iw_info, get_wifi_signal_strength, get_wifi_info
    from linux.security import NetworkSecurityCheck


class ReportManager:
    def __init__(self, filename="network_diagnostic_report.txt"):
        self.filename = filename
        self.content = []

    def append_to_report(self, text):
        """Appends given text to the report content list."""
        self.content.append(text)

    def save_report(self):
      if not self.content:
        print("Error: Report content is empty.")
        return

    # Convert all items in content to strings and join them with newline for better formatting
      with open(self.filename, "w") as file:
        file.writelines(str(line) + "\n" for line in self.content)

    def email_report(self, recipient_email):
        """Emails the report file to the specified email."""
        sender_email = "MS_Pvh4Gm@trial-zr6ke4nn7v34on12.mlsender.net"
        smtp_server = "smtp.mailersend.net"
        smtp_port = 587  # TLS port
        smtp_user = "MS_Pvh4Gm@trial-zr6ke4nn7v34on12.mlsender.net"
        smtp_password = "u5NttfFgmP0TZl09"  # Replace with your App Password

        try:
            # Create the email message
            msg = EmailMessage()
            msg["Subject"] = "Network Analysis Report"
            msg["From"] = formataddr(("Report Manager", sender_email))
            msg["To"] = recipient_email
            msg.set_content("Please find the attached network analysis report.")

            # Attach the report file
            with open(self.filename, "rb") as file:
                file_data = file.read()
                file_name = os.path.basename(self.filename)
                msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

            # Connect to the SMTP server and send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Upgrade the connection to TLS
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
            print(f"Report sent successfully to {recipient_email}")
        except Exception as e:
            print(f"Error sending email: {e}")

    def save_and_email_report(self):
        """Saves the report to a file and optionally emails it."""
        self.save_report()
        recipient_email = input("Enter the recipient email address (or leave blank to skip): ").strip()
        
        if recipient_email:
            self.email_report(recipient_email)
        else:
            print("No email entered. Report saved locally.")

def run_all_tests(report_manager):
    # Run network connectivity tests
    try:
        report_manager.append_to_report("Ping Test Result:")
        report_manager.append_to_report(ping_test("8.8.8.8"))
    except Exception as e:
        report_manager.append_to_report(f"Ping Test failed: {e}")

    try:
        report_manager.append_to_report("DNS Lookup Result:")
        report_manager.append_to_report(dns_lookup("www.google.com"))
    except Exception as e:
        report_manager.append_to_report(f"DNS Lookup failed: {e}")

    try:
        report_manager.append_to_report("Traceroute Result:")
        report_manager.append_to_report(trace_route("8.8.8.8"))
    except Exception as e:
        report_manager.append_to_report(f"Traceroute failed: {e}")

    # Run speed test
    try:
        report_manager.append_to_report("Speed Test Result:")
        report_manager.append_to_report(speed_test())
    except Exception as e:
        report_manager.append_to_report(f"Speed Test failed: {e}")

    try:
        report_manager.append_to_report("WiFi Interface Information:")
        report_manager.append_to_report(get_wireless_interface())
    except Exception as e:
        report_manager.append_to_report(f"WiFi Interface Information retrieval failed: {e}")

    try:
        report_manager.append_to_report(get_iw_info())
    except Exception as e:
        report_manager.append_to_report(f"WiFi Interface Info retrieval failed: {e}")

    try:
        report_manager.append_to_report("WiFi Signal Strength:")
        report_manager.append_to_report(get_wifi_signal_strength())
    except Exception as e:
        report_manager.append_to_report(f"WiFi Signal Strength retrieval failed: {e}")

    try:
        report_manager.append_to_report("WiFi Details:")
        report_manager.append_to_report(get_wifi_info())
    except Exception as e:
        report_manager.append_to_report(f"WiFi Details retrieval failed: {e}")

    # Network security check
    try:
        report_manager.append_to_report("Network Security Check:")
        report_manager.append_to_report(NetworkSecurityCheck().nmap_scan("8.8.8.8", 300))
        report_manager.append_to_report(NetworkSecurityCheck().firewall_detection("8.8.8.8", 300))
        report_manager.append_to_report(NetworkSecurityCheck().ssl_tls_inspection("www.google.com"))
    except Exception as e:
        report_manager.append_to_report(f"Network Security Check failed: {e}")

    print("All tests have been run and appended to the report.")

def run():
    print("running tests.....")
    # Initialize the report manager
    report_manager = ReportManager("network_diagnostic_report.txt")
    
    # Run all tests and append their results to the report
    run_all_tests(report_manager)
    
    # Save the report locally and prompt the user for email option
    report_manager.save_and_email_report()

if __name__ == "__main__":
    run()
