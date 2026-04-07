#!/bin/bash
# Sets up Redis for inter-node IPC.
# Persistence is disabled to protect the hard drive / SD card from wear.

set -e

sudo apt update
sudo apt upgrade -y
sudo apt install -y redis-server hostapd dnsmasq

sudo systemctl start redis-server
sudo systemctl enable redis-server

ROBUS_CORE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REDIS_CONF=/etc/redis/redis.conf

if grep -q "^save" "$REDIS_CONF"; then
    sudo sed -i 's/^save .*/save ""/' "$REDIS_CONF"
else
    echo 'save ""' | sudo tee -a "$REDIS_CONF" > /dev/null
fi

if grep -q "^appendonly" "$REDIS_CONF"; then
    sudo sed -i 's/^appendonly .*/appendonly no/' "$REDIS_CONF"
else
    echo 'appendonly no' | sudo tee -a "$REDIS_CONF" > /dev/null
fi

# Activate redis over hotspot
sudo python3 "$ROBUS_CORE/utils/web_redis.py"

sudo systemctl restart redis-server

echo "Redis setup complete. Persistence disabled."
