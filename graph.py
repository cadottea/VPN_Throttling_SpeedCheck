import os
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd


def parse_speed_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                # Extract both download and upload speeds
                if "Download:" in line and "Upload:" in line:
                    date_str = line.split(" - ")[0]
                    download_speed = float(re.search(r"Download: ([\d.]+)", line).group(1))
                    upload_speed = float(re.search(r"Upload: ([\d.]+)", line).group(1))
                    date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                    data.append((date, download_speed, upload_speed))
            except (ValueError, AttributeError):
                print(f"Skipping invalid line in {file_path}: {line.strip()}")
    return data


def process_all_folders(base_path):
    all_data = []
    print(f"Scanning base path: {base_path}")
    for folder_name in os.listdir(base_path):
        print(f"Checking folder: {folder_name}")
        if re.fullmatch(r'\d{4,5}', folder_name):  # Match folder names with 4 or 5 digits
            folder_path = os.path.join(base_path, folder_name)
            print(f"Processing folder: {folder_name}")
            for file_name in os.listdir(folder_path):
                if file_name.endswith("_speed_data.txt") or file_name.endswith("_speed_data_vpn.txt"):
                    is_vpn = "VPN" if "vpn" in file_name.lower() else "Standard"
                    file_path = os.path.join(folder_path, file_name)
                    print(f"Processing file: {file_path}")
                    if os.path.exists(file_path):
                        data = parse_speed_data(file_path)
                        for date, download_speed, upload_speed in data:
                            all_data.append((folder_name, date.date(), download_speed, upload_speed, is_vpn))
    if not all_data:
        print("No valid data found in any folder.")
    return pd.DataFrame(all_data, columns=["Server", "Date", "Download_Speed", "Upload_Speed", "Connection"])


def plot_speeds(df):
    # Calculate daily averages
    df_avg = df.groupby(["Server", "Date", "Connection"], as_index=False).mean()

    plt.figure(figsize=(14, 8))
    for server in df_avg["Server"].unique():
        for connection in df_avg["Connection"].unique():
            server_data = df_avg[(df_avg["Server"] == server) & (df_avg["Connection"] == connection)]
            if not server_data.empty:
                # Plot download speeds
                plt.plot(
                    server_data["Date"],
                    server_data["Download_Speed"],
                    marker='o',
                    label=f"Server {server} ({connection}) - Download"
                )
                # Plot upload speeds
                plt.plot(
                    server_data["Date"],
                    server_data["Upload_Speed"],
                    marker='x',
                    linestyle='--',
                    label=f"Server {server} ({connection}) - Upload"
                )

    # Add gridlines
    plt.grid(axis='y', linestyle='--', linewidth=0.7, alpha=0.7)

    # Format x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.xticks(rotation=45)

    # Add labels, title, and legend
    plt.xlabel("Date")
    plt.ylabel("Speed (Mbps)")
    plt.title("Daily Average Internet Speeds by Server and Connection Type")
    plt.legend(title="Server (Connection)", bbox_to_anchor=(1.05, 1), loc='upper left')

    # Add clear Mbps markings on the y-axis
    max_speed = int(max(df["Download_Speed"].max(), df["Upload_Speed"].max())) + 10
    plt.yticks(range(0, max_speed, 10))

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    base_path = "./server_results"  # Adjust base path as necessary
    df = process_all_folders(base_path)
    if not df.empty:
        plot_speeds(df)
    else:
        print("No valid data found.")