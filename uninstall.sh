#!/bin/sh

# Error out if anything fails.
set -e

# Make sure script is run as root.
if [ "$(id -u)" != "0" ]; then
  echo "Must be run as root with sudo! Try: sudo ./uninstall.sh"
  exit 1
fi

CURRENT_DIR=$(pwd)
SCRIPT_DIR=$(dirname $0)

if [ $SCRIPT_DIR = '.' ]
then
  SCRIPT_DIR="$CURRENT_DIR"
fi

echo "Remove /etc/systemd/system/stilas-usb-mount@.service..."
echo "========================="
rm /etc/systemd/system/stilas-usb-mount@.service

echo "Remove /etc/udev/rules.d/90-stilas-detect-storage.rules..."
echo "========================="
rm /etc/udev/rules.d/90-stilas-detect-storage.rules

echo "Restart udev and systemctl"
echo "========================="
service udev restart
systemctl daemon-reload

echo "Finished!"
