import os
import re
from datetime import datetime
import pandas as pd
from scipy.stats import ttest_ind


def parse_speed_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                if "Download:" in line and "Upload:" in line:
                    date_str = line.split(" - ")[0]
                    download_speed = float(re.search(r"Download: ([\d.]+)", line).group(1))
                    upload_speed = float(re.search(r"Upload: ([\d.]+)", line).group(1))
                    date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                    data.append((date, download_speed, upload_speed))
            except (ValueError, AttributeError):
                pass  # Skip invalid lines
    return data


def process_all_folders(base_path):
    all_data = []
    for folder_name in os.listdir(base_path):
        if re.fullmatch(r'\d{4,5}', folder_name):  # Match folder names with 4 or 5 digits
            folder_path = os.path.join(base_path, folder_name)
            for file_name in os.listdir(folder_path):
                if file_name.endswith("_speed_data.txt") or file_name.endswith("_speed_data_vpn.txt"):
                    is_vpn = "VPN" if "vpn" in file_name.lower() else "Standard"
                    file_path = os.path.join(folder_path, file_name)
                    if os.path.exists(file_path):
                        data = parse_speed_data(file_path)
                        for date, download_speed, upload_speed in data:
                            all_data.append((download_speed, upload_speed, is_vpn))
    return pd.DataFrame(all_data, columns=["Download_Speed", "Upload_Speed", "Connection"])


def calculate_statistical_significance(df):
    vpn_data = df[df["Connection"] == "VPN"]
    non_vpn_data = df[df["Connection"] == "Standard"]

    results = {}
    for metric in ["Download_Speed", "Upload_Speed"]:
        vpn_speeds = vpn_data[metric]
        non_vpn_speeds = non_vpn_data[metric]

        # Perform t-test
        t_stat, p_value = ttest_ind(vpn_speeds, non_vpn_speeds, equal_var=False)

        # Store results
        results[metric] = {
            "VPN Mean": vpn_speeds.mean(),
            "Non-VPN Mean": non_vpn_speeds.mean(),
            "Difference": non_vpn_speeds.mean() - vpn_speeds.mean(),
            "t-Statistic": t_stat,
            "p-Value": p_value,
            "Significant": p_value < 0.05
        }
    return results


if __name__ == "__main__":
    base_path = "./server_results"  # Adjust base path if necessary
    df = process_all_folders(base_path)
    
    if not df.empty:
        results = calculate_statistical_significance(df)
        
        # Print results
        print("\nStatistical Significance Results:\n")
        for metric, stats in results.items():
            print(f"{metric}:")
            for key, value in stats.items():
                print(f"  {key}: {value:.4f}" if isinstance(value, float) else f"  {key}: {value}")
            print()
    else:
        print("No valid data found.")