# Internet Throttling Detection Project

## Overview

The **Internet Throttling Detection Project** is an automated system designed to test internet speeds and analyze the impact of VPN usage. Whether you’re looking to uncover ISP throttling or understand how a VPN affects your connection, this project dynamically tests and organizes results, providing clear insights through graphs and comparisons.

## Features

- **Dynamic Server Management**:
  - Automatically detects or generates a list of 10 active servers for testing.
  - Organizes server results in an easily navigable structure.
  
- **VPN Awareness**:
  - Detects VPN status and tags results with “VPN” for streamlined analysis.  
    **NOTE**: My VPN uses IPv4, and my regular provider uses IPv6. I use this difference to determine whether my VPN is active, but your case may differ!
  - Compares VPN and non-VPN performance to identify potential throttling.
  
- **Automated Data Collection**:
  - Saves date-stamped test results, including download and upload speeds, in the `server_results` folder.
  - Handles folder creation and data organization seamlessly.
  
- **Insightful Analysis**:
  - Visualize daily speed trends using the `graph` module.
  - Use `graph.py difference_vpn` to statistically compare VPN vs. non-VPN performance on a day-to-day basis.  
    **NOTE**: You can only run this program a few times within a short frame of time, or the servers will begin blocking your noisy traffic. I did not find a workaround to this, but it still works fine if you just run it once or twice an hour to collect statistics on VPN vs. Non-VPN speeds.

### Future Features

- Background running feature to check VPN vs. Non-VPN speeds at least once a day.

## How It Works

### Testing Internet Speeds

1. Run `main.py`:
   - If the `available_servers` folder exists, it uses the listed servers to perform speed tests.
   - If the folder is missing, it dynamically generates a new list of 10 servers using `how_many_available.py`.
2. During tests, VPN status is checked via `check_vpn.py`:
   - Results are tagged as “VPN” if active or left untagged otherwise.
3. Results are saved, categorized by server number, in the `server_results` folder, which is automatically created if it doesn’t exist.

### Refreshing Server Lists

- Over time, servers may go offline. Delete the `available_servers` folder to regenerate a fresh list during the next run.

### Analyzing Results

- **Graphical Insights**:
  - Use `graph.py` to plot daily averages of download and upload speeds.
- **Detecting Throttling**:
  - Use `difference_vpn.py` to calculate the net difference between VPN and non-VPN speeds, revealing potential throttling.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/internet-throttling-detection.git
   cd internet-throttling-detection

    2.  Install required Python packages:
    pip install -r requirements.txt


  3.  Ensure the following modules are included in the project directory:
  • main.py (or whatever most recent version is available)
  • versioning.py
  • test_specific.py
  • check_vpn.py
  • how_many_available.py
  • graph.py
  • difference_vpn.py

## Usage

### Run the Main Program (with and without your VPN active)
```bash
python main.py

Plot Results
python graph.py

Calculate VPN vs. Non-VPN Differences
python difference_vpn.py

### File Structure

- available_servers: Contains the current list of servers for testing. Automatically created and refreshed as needed.
- server_results: Stores speed test results organized by server ID.
- main.py: The primary script to run speed tests.
- versioning.py: Dynamically imports the latest version of each module.
- graph.py: Generates visual representations of test results.
- difference_vpn.py: Compares VPN and non-VPN performance.

Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for improvements or new features.

License

This project is licensed under the MIT License.

Disclaimer

This project is intended for educational and informational purposes only. The user assumes all responsibility for its use.