#!/bin/bash
SSID=$1
PSK=$2

# manage the connection with wpa_cli
/sbin/wpa_cli -i wlan0 disconnect
/sbin/wpa_cli -i wlan0 remove_network 0
/sbin/wpa_cli -i wlan0 add_network
/sbin/wpa_cli -i wlan0 set_network 0 ssid \"$SSID\"
/sbin/wpa_cli -i wlan0 set_network 0 psk \"$PSK\"
/sbin/wpa_cli -i wlan0 enable_network 0
/sbin/wpa_cli -i wlan0 reconnect
