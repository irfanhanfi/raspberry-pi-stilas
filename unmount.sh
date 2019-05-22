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

umount /media/pi/sdb1/
