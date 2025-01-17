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
        return False  # Default to not active if unable to fetch IP

    try:
        # Check if the IP is IPv4 or IPv6
        ip_obj = ipaddress.ip_address(current_ip)
        return ip_obj.version == 4  # Assume VPN is active for IPv4
    except ValueError:
        return False  # Invalid IP address, default to not active

if __name__ == "__main__":
    vpn_active = is_vpn_active()
    if vpn_active:
        print("VPN is active.")
    else:
        print("No VPN detected.")