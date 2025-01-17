import speedtest
import os

# Function to test a specific server by server ID, host, and port
def test_specific_server(server_id, server_host, server_port):
    st = speedtest.Speedtest()

    # Manually set the server details directly
    st._server = {'id': server_id, 'host': server_host, 'port': server_port}
    
    try:
        # Test download speed
        print(f"Testing download speed on Server ID: {server_id}, Host: {server_host}, Port: {server_port}")
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        print(f"Download Speed: {download_speed:.2f} Mbps")
        
        # Test upload speed
        print(f"Testing upload speed on Server ID: {server_id}, Host: {server_host}, Port: {server_port}")
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        print(f"Upload Speed: {upload_speed:.2f} Mbps")

        return {
            "id": server_id,
            "host": server_host,
            "port": server_port,
            "download_speed": download_speed,
            "upload_speed": upload_speed,
        }
    except Exception as e:
        print(f"An error occurred while testing server {server_id}: {e}")
        return None

# Function to read servers from available_servers.txt
def load_servers(file_path):
    servers = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 3:  # Ensure the line has exactly 3 parts
                    server_id = int(parts[0])
                    server_host = parts[1]
                    server_port = int(parts[2])
                    servers.append({"id": server_id, "host": server_host, "port": server_port})
    except Exception as e:
        print(f"An error occurred while loading servers: {e}")
    return servers

# Main function to test all servers in available_servers.txt
if __name__ == "__main__":
    available_servers_file = os.path.join(os.getcwd(), "available_servers", "available_servers.txt")

    if not os.path.exists(available_servers_file):
        print(f"Server file not found: {available_servers_file}")
    else:
        servers = load_servers(available_servers_file)
        if not servers:
            print("No servers loaded from the file.")
        else:
            print(f"Loaded {len(servers)} servers. Starting tests...")
            results = []
            for server in servers:
                result = test_specific_server(server["id"], server["host"], server["port"])
                if result:
                    results.append(result)

            print("\nTest Results:")
            for result in results:
                print(
                    f"Server ID: {result['id']}, Host: {result['host']}, Port: {result['port']}, "
                    f"Download: {result['download_speed']:.2f} Mbps, Upload: {result['upload_speed']:.2f} Mbps"
                )