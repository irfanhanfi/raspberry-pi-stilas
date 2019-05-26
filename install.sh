#!/bin/sh

# Error out if anything fails.
set -e

# Make sure script is run as root.
if [ "$(id -u)" != "0" ]; then
  echo "Must be run as root with sudo! Try: sudo ./install.sh"
  exit 1
fi

CURRENT_DIR=$(pwd)
SCRIPT_DIR=$(dirname $0)

if [ $SCRIPT_DIR = '.' ]
then
  SCRIPT_DIR="$CURRENT_DIR"
fi

echo "Installing dependencies..."
echo "=========================="
apt update && apt -y install python3 ntfs-3g chromium-browser

echo "Create usb-mount@.service File..."
echo "========================="
cat << EOF > "$SCRIPT_DIR/stilas-usb-mount@.service"
[Unit]
Description=Mount USB Drive on %i
[Service]
Type=oneshot
RemainAfterExit=true
ExecStart=${SCRIPT_DIR}/stilas-usb-mount.sh add %i
ExecStop=${SCRIPT_DIR}/stilas-usb-mount.sh remove %i
EOF

echo "Move usb-mount@.service File..."
echo "========================="
mv "$SCRIPT_DIR/stilas-usb-mount@.service" /etc/systemd/system/stilas-usb-mount@.service

echo "Create 90-stilas-detect-storage.rules File..."
echo "========================="
cat << EOF > "$SCRIPT_DIR/90-stilas-detect-storage.rules"
KERNEL=="sd[a-z][0-9]", SUBSYSTEMS=="usb", ACTION=="add", RUN+="/bin/systemctl start stilas-usb-mount@%k.service"
KERNEL=="sd[a-z][0-9]", SUBSYSTEMS=="usb", ACTION=="remove", RUN+="/bin/systemctl stop stilas-usb-mount@%k.service"
EOF

echo "Move 90-stilas-detect-storage.rules File..."
echo "========================="
mv "$SCRIPT_DIR/90-stilas-detect-storage.rules" /etc/udev/rules.d/90-stilas-detect-storage.rules


echo "Restart udev and systemctl"
echo "========================="
service udev restart
#~ udevadm control --reload-rules
systemctl daemon-reload

echo "Make files executable..."
echo "========================="
chmod +x $SCRIPT_DIR/start.sh
chmod +x $SCRIPT_DIR/stilas-usb-mount.sh
chmod +x $SCRIPT_DIR/stilas/wifi-connect.sh
chmod +x $SCRIPT_DIR/stilas/set_boot_config.sh

echo "Finished!"
