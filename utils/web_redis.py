import os
import subprocess
import sys
import time

# --- Configuration ---
SSID = "Pi_Redis_Net"
WIFI_PASS = "password123"
HOTSPOT_IP = "192.168.4.1"
REDIS_CONF = "/etc/redis/redis.conf"

def run(cmd):
    """Utility to run shell commands."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[!] Error running: {cmd}\n{result.stderr}")
    return result

def setup_hotspot():
    print("[*] Installing core dependencies...")
    run("apt-get update && apt-get install -y hostapd dnsmasq")

    # 1. Stop services to configure them
    run("systemctl stop hostapd dnsmasq")

    # 2. Configure Static IP via dhcpcd.conf
    print("[*] Setting static IP 192.168.4.1...")
    with open("/etc/dhcpcd.conf", "a") as f:
        # Check if already configured to avoid double-entry
        f.write(f"\ninterface wlan0\n    static ip_address={HOTSPOT_IP}/24\n    nohook wpa_supplicant\n")

    # 3. Configure DHCP Server (dnsmasq)
    print("[*] Configuring DHCP range for ESP...")
    dns_conf = f"""interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
domain=wlan
address=/gw.lan/{HOTSPOT_IP}
"""
    with open("/etc/dnsmasq.conf", "w") as f:
        f.write(dns_conf)

    # 4. Configure Access Point (hostapd)
    print(f"[*] Setting SSID: {SSID}...")
    hostapd_conf = f"""interface=wlan0
driver=nl80211
ssid={SSID}
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
wpa_passphrase={WIFI_PASS}
"""
    with open("/etc/hostapd/hostapd.conf", "w") as f:
        f.write(hostapd_conf)

    # Point the system to the config file
    run("sed -i 's|#DAEMON_CONF=\"\"|DAEMON_CONF=\"/etc/hostapd/hostapd.conf\"|' /etc/default/hostapd")

    # 5. Unmask and Enable
    run("systemctl unmask hostapd")
    run("systemctl enable hostapd dnsmasq")
    run("rfkill unblock wlan")

def setup_redis():
    print("[*] Opening Redis to the hotspot network...")
    if os.path.exists(REDIS_CONF):
        with open(REDIS_CONF, "r") as f:
            lines = f.readlines()
        
        with open(REDIS_CONF, "w") as f:
            for line in lines:
                if line.strip().startswith("bind 127.0.0.1"):
                    # Bind to both local and hotspot IP
                    f.write(f"bind 127.0.0.1 {HOTSPOT_IP}\n")
                elif line.strip().startswith("protected-mode"):
                    f.write("protected-mode no\n")
                elif line.strip().startswith("requirepass"):
                    f.write(f"# {line}") # Disable password
                else:
                    f.write(line)
        
        run("systemctl restart redis-server")
        print("[+] Redis configured for open access.")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Please run this script with 'sudo python3 script_name.py'")
        sys.exit(1)

    setup_hotspot()
    setup_redis()
    
    print("\n" + "="*40)
    print("SUCCESS: Gateway Setup Complete")
    print(f"SSID: {SSID}")
    print(f"Password: {WIFI_PASS}")
    print(f"Redis IP: {HOTSPOT_IP}")
    print("="*40)
    print("REBOOT RECOMMENDED for networking changes to take full effect.")