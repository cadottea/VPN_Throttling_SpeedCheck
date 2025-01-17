import os
import versioning

def main():
    # Get the current directory
    current_directory = os.getcwd()

    # Import the latest version of check_vpn via versioning
    check_vpn = versioning.import_module(current_directory, "check_vpn")

    # Determine VPN status
    vpn_active = check_vpn.is_vpn_active()  # No arguments passed
    tag = "vpn" if vpn_active else ""

    # Inform the user about VPN status
    print(f"VPN is {'active' if vpn_active else 'not active'}. Tag: {tag}")

    # Import the latest versions of test_specific, output_results, and how_many_available via versioning
    test_specific = versioning.import_module(current_directory, "test_specific")
    output_results = versioning.import_module(current_directory, "output_results")
    how_many_available = versioning.import_module(current_directory, "how_many_available")

    # Path to the available_servers.txt file
    available_servers_file = os.path.join(current_directory, "available_servers", "available_servers.txt")

    # Check if the file exists, or call how_many_available to generate it
    if not os.path.exists(available_servers_file):
        print(f"Server file not found: {available_servers_file}")
        print("Generating available_servers.txt using how_many_available...")
        how_many_available.generate_available_servers(available_servers_file)
    
    if not os.path.exists(available_servers_file):
        print("Failed to generate available_servers.txt. Exiting.")
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
            output_results.save_results(result, tag)  # Pass the tag based on VPN status

    print("\nTest Results:")
    for result in results:
        print(
            f"Server ID: {result['id']}, Host: {result['host']}, Port: {result['port']}, "
            f"Download: {result['download_speed']:.2f} Mbps, Upload: {result['upload_speed']:.2f} Mbps"
        )

if __name__ == "__main__":
    main()