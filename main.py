import os
import argparse
import versioning

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Speed test program with optional VPN tagging.")
    parser.add_argument('tag', nargs='?', default='', help="Optional tag for results (e.g., 'vpn')")
    args = parser.parse_args()

    # Get the current directory
    current_directory = os.getcwd()

    # Import the latest versions of test_specific and output_results
    test_specific = versioning.import_module(current_directory, "test_specific")
    output_results = versioning.import_module(current_directory, "output_results")

    # Path to the available_servers.txt file
    available_servers_file = os.path.join(current_directory, "available_servers", "available_servers.txt")

    if not os.path.exists(available_servers_file):
        print(f"Server file not found: {available_servers_file}")
        return

    # Load servers from the available_servers.txt file
    servers = test_specific.load_servers(available_servers_file)
    if not servers:
        print("No servers loaded from the file.")
        return

    print(f"Loaded {len(servers)} servers. Starting tests...")

    # Run tests on each server and collect results
    results = []
    for server in servers:
        result = test_specific.test_specific_server(
            server["id"], server["host"], server["port"]
        )
        if result:
            results.append(result)
            output_results.save_results(result, args.tag)  # Pass the tag to save_results

    print("\nTest Results:")
    for result in results:
        print(
            f"Server ID: {result['id']}, Host: {result['host']}, Port: {result['port']}, "
            f"Download: {result['download_speed']:.2f} Mbps, Upload: {result['upload_speed']:.2f} Mbps"
        )

if __name__ == "__main__":
    main()