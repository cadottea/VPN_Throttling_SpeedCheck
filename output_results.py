import os
from datetime import datetime

# Define the base directory for storing results
BASE_DIR = os.path.join(os.getcwd(), "server_results")

def save_results(server):
    """
    Saves speed test results to a file inside a server-specific folder.
    """
    try:
        server_id = server['id']
        download_speed = server['download_speed']
        upload_speed = server['upload_speed']
        
        # Construct server folder path
        server_folder = os.path.join(BASE_DIR, str(server_id))
        os.makedirs(server_folder, exist_ok=True)  # Create folder if it doesn't exist
        
        # Define the file path
        file_path = os.path.join(server_folder, f"{server_id}_speed_data.txt")
        
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