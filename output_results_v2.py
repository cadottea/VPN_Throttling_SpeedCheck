import os
from datetime import datetime

# Define the base directory for storing results
BASE_DIR = os.path.join(os.getcwd(), "server_results")

def save_results(server, tag=''):
    """
    Saves speed test results to a file inside a server-specific folder, optionally appending a tag.
    """
    try:
        server_id = server['id']
        download_speed = server['download_speed']
        upload_speed = server['upload_speed']
        
        # Construct server folder path
        server_folder = os.path.join(BASE_DIR, str(server_id))
        os.makedirs(server_folder, exist_ok=True)  # Create folder if it doesn't exist
        
        # Define the file name and path
        file_name = f"{server_id}_speed_data"
        if tag:
            file_name += f"_{tag}"  # Append the tag if provided
        file_name += ".txt"
        file_path = os.path.join(server_folder, file_name)
        
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Format the entry
        entry = f"{timestamp} - Download: {download_speed:.2f} Mbps, Upload: {upload_speed:.2f} Mbps\n"
        
        # Append the entry to the file
        with open(file_path, 'a') as file:
            file.write(entry)
        
        print(f"Data written to {file_path}")
    except Exception as e:
        print(f"Error saving results for server {server.get('id', 'unknown')}: {e}")