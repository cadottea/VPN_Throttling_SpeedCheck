import os
import speedtest

# Create a Speedtest object
st = speedtest.Speedtest()

# Fetch and list all servers
servers = st.get_servers()  # Retrieves all servers, not just the closest ones
server_list = [server for sublist in servers.values() for server in sublist]

# Create the 'available_servers' directory if it doesn't exist
os.makedirs('available_servers', exist_ok=True)

# Create a file to dump the server information
file_path = os.path.join('available_servers', 'available_servers.txt')

# Open the file in write mode
with open(file_path, 'w') as file:
    # Write only the required server details
    for server in server_list[:10]:  # Limit to 10 for readability
        # Extract required server details
        server_id = server.get('id', 'N/A')
        server_host = server.get('host', 'N/A').split(':')[0]  # Remove the port from the host
        server_port = server.get('port', 8080)

        # Format the line
        line = f"{server_id} {server_host} {server_port}"
        
        # Write to the file
        file.write(line + "\n")
        
        # Print to the terminal
        print(line)

print(f"Server information has been saved to {file_path}")