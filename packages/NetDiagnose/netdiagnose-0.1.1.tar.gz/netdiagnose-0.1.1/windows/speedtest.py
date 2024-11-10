import speedtest
import time
import statistics


def speed_test(self):
        """Perform internet speed test"""
        try:
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


            print(f"\nNetwork Speed Test Results:")
            print(f"Download Speed: {download_speed:.2f} Mbps")
            print(f"Upload Speed: {upload_speed:.2f} Mbps")
            print(f"Ping: {ping:.2f} ms")
            print(f"Jitter: {jitter:.2f} ms")


        except Exception as e:
            return False, f"Speed test failed: {str(e)}"