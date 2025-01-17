import requests

def is_vpn_active():
    """Check if the current public IP belongs to a VPN provider."""
    try:
        response = requests.get("https://ipinfo.io", timeout=5)
        response.raise_for_status()
        data = response.json()

        # Get ASN and ISP details
        org = data.get("org", "")
        ip = data.get("ip", "")

        print(f"Current IP: {ip}")
        print(f"Organization: {org}")

        # Check if the organization name includes common VPN terms
        vpn_keywords = ["VPN", "Proxy", "Hosting", "CyberGhost", "NordVPN"]
        if any(keyword in org for keyword in vpn_keywords):
            print("VPN is active.")
            return True
        else:
            print("No VPN detected.")
            return False
    except requests.RequestException as e:
        print(f"Error determining VPN status: {e}")
        return False

# Run the check
is_vpn_active()