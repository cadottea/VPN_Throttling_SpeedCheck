import requests
import ipaddress

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

def is_vpn_active():
    """Check VPN status based on public IP address type."""
    current_ip = get_public_ip()
    if not current_ip:
        print("Unable to determine public IP.")
        return False

    try:
        # Check if the IP is IPv4 or IPv6
        ip_obj = ipaddress.ip_address(current_ip)
        if ip_obj.version == 4:
            print(f"Current IP: {current_ip} (IPv4) - VPN is active.")
            return True  # VPN is likely active
        elif ip_obj.version == 6:
            print(f"Current IP: {current_ip} (IPv6) - VPN is not active.")
            return False  # VPN is likely inactive
    except ValueError:
        print("Invalid IP address detected.")
        return False

# Example usage
if is_vpn_active():
    print("VPN is active.")
else:
    print("VPN is not active.")