import os
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd


def parse_speed_data(file_path):
    """Parse speed data from a file."""
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
    """Process all folders in the base path for speed data."""
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


def plot_daily_averages_with_error_bars(df):
    """Plot daily averages with error bars for VPN and non-VPN data."""
    # Group by Date and Connection, calculate mean and standard deviation
    grouped = df.groupby(["Date", "Connection"]).agg(
        avg_download=("Download_Speed", "mean"),
        std_download=("Download_Speed", "std"),
        avg_upload=("Upload_Speed", "mean"),
        std_upload=("Upload_Speed", "std")
    ).reset_index()

    plt.figure(figsize=(12, 6))
    for connection in grouped["Connection"].unique():
        connection_data = grouped[grouped["Connection"] == connection]

        # Plot download speeds with error bars (no connecting lines)
        plt.errorbar(
            connection_data["Date"],
            connection_data["avg_download"],
            yerr=connection_data["std_download"],
            fmt='o',  # Points only
            label=f"{connection} - Download",
            capsize=5,
            linestyle='none'  # No connecting lines
        )

        # Plot upload speeds with error bars (no connecting lines)
        plt.errorbar(
            connection_data["Date"],
            connection_data["avg_upload"],
            yerr=connection_data["std_upload"],
            fmt='x',  # Points only
            label=f"{connection} - Upload",
            capsize=5,
            linestyle='none'  # No connecting lines
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
    plt.title("Daily Average Speeds with Error Bars by Connection Type")
    plt.legend(title="Connection Type", bbox_to_anchor=(1.05, 1), loc='upper left')

    # Add clear Mbps markings on the y-axis
    max_speed = int(max(grouped["avg_download"].max(), grouped["avg_upload"].max())) + 10
    plt.yticks(range(0, max_speed, 10))

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    base_path = "./server_results"  # Adjust base path as necessary
    df = process_all_folders(base_path)
    if not df.empty:
        plot_daily_averages_with_error_bars(df)
    else:
        print("No valid data found.")