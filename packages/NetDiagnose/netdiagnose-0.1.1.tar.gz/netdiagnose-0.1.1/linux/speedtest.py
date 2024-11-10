import speedtest
import time
import statistics
import socket

def speed_test():
        try:
            print("Starting speed test.....")
            st = speedtest.Speedtest()
            server = st.get_best_server()
            print("Testing download speed...")
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            print("Testing upload speed...")
            upload_speed = st.upload() / 1_000_000  # Convert to Mbps
            print("Measuring ping and jitter...")
            ping_times = []
            for _ in range(10):  # Take 10 ping samples
                ping = st.results.ping
                ping_times.append(ping)
                time.sleep(0.2)  # Small delay between pings
            # Calculate jitter as the standard deviation of ping times
            jitter = statistics.stdev(ping_times) if len(ping_times) > 1 else 0

            return( f"\nNetwork Speed Test Results: \n"
                   f"Server located in {server['name']}, {server['country']} \n"
                   f"Download Speed: {download_speed:.2f} Mbps \n"
                   f"Upload Speed: {upload_speed:.2f} Mbps \n"
                   f"Ping: {ping:.2f} ms \n"
                   f"Jitter: {jitter:.2f} ms \n")
        except speedtest.ConfigRetrievalError as e:
            return(f"Error retrieving speed test configuration: {e}")
        except socket.gaierror as e:
            return(f"DNS resolution error: {e}")
        except Exception as e:
            return(f"An unexpected error occurred: {e}")



