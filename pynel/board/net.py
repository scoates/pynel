import time
from network import WLAN, STA_IF


def wifi_connect(config):
    station = WLAN(STA_IF)

    if station.isconnected():
        print("Already connected")
        return

    print(f"Connecting to {config['NET_SSID']}")
    station.active(True)
    station.connect(config["NET_SSID"], config["NET_PASS"])

    while not station.isconnected():
        time.sleep(1)
        print("...still connecting...")

    print("Connection successful")
    print(station.ifconfig())
