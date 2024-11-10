# NetDiagnose

A comprehensive network diagnostic tool for both Linux and Windows platforms, designed to test and analyze various network components, including:

- Ping test
- DNS lookup
- Traceroute
- Speed test
- Network interfaces information
- Wireless network analysis
- Port scanning
- Network security checks

## Features

- **Ping Test**: Test the connectivity to a given destination.
- **DNS Lookup**: Resolve domain names to IP addresses.
- **Traceroute**: Trace the route packets take to a destination.
- **Network Speed Test**: Measure your internet's download and upload speeds.
- **Network Interface Info**: Get details about your network interfaces, including IP address, MAC address, and status.
- **Wireless Network Analysis**: Analyze Wi-Fi signal strength, interfaces, and more (Linux-specific).
- **Port Scan**: Scan open ports on a given host (Linux and Windows support).
- **Network Security Check**: Scan for potential vulnerabilities in the network configuration.
- **Generate and Save a Report**: Ability to Scan and save a report of all test to your device or email the report to yourself.
## Installation

To get started with the network diagnostic tool, follow the installation steps below:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/gentlsnek/NetDiagnose
    cd NetDiagnose
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the Tool

After installation, you can run the network diagnostic tool by executing the `main.py` file:

```bash
python main.py
