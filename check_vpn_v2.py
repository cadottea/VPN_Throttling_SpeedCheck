import requests

def get_public_ip():
    """Fetch the current public IP using multiple services."""
    services = [
        "https://icanhazip.com",
        "https://api.ipify.org",
        "https://checkip.amazonaws.com"
    ]
    for service in services:
        try:
            response = requests.get(service, timeout=5)
            response.raise_for_status()
            return response.text.strip()
        except requests.RequestException:
            continue
    return None

def is_vpn_active(known_non_vpn_ip):
    """Check if the current public IP differs from the known non-VPN IP."""
    current_ip = get_public_ip()
    if not current_ip:
        print("Unable to determine public IP.")
        return False

    print(f"Current Public IP: {current_ip}")
    if current_ip != known_non_vpn_ip:
        return True  # IP has changed, likely due to VPN
    return False

# Replace this with your actual non-VPN IP
known_non_vpn_ip = "2601:40f:4480:7340:fc43:eb9a:78a1:22c5"

if is_vpn_active(known_non_vpn_ip):
    print("VPN is active.")
else:
    print("No VPN detected.")