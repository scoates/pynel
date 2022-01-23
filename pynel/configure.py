import json
import sys
import os
import logging

DIR = os.path.realpath(os.path.dirname(__file__))

log = logging.getLogger()
log_level = os.environ.get("LOG_LEVEL")
if log_level is None:
    logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
else:
    logging.basicConfig(stream=sys.stdout, level=getattr(logging, log_level))
    log.debug(f"Set log level to {log_level}")


def _boolish(val):
    if str(val).lower() in ("true", "1"):
        return True
    return False


def _percent(val):
    try:
        val = int(val)
    except ValueError:
        val = 50
    if 0 < val < 100:
        return val
    else:
        return 50


KEYS = {
    "NET_SSID": ("Wifi SSID", str),
    "NET_PASS": ("Wifi Password", str),
    "DATA_PIN": ("LED Panel data pin number", int),
    "PIXELS_W": ("Panel is this many pixels wide", int),
    "PIXELS_H": ("Panel is this many pixels tall", int),
    "SERPENTINE": ("Panel is laid out out in a zig-zag pattern", _boolish),
    "BRIGHTNESS": ("Panel brightness is scaled to this value (0-100)", _percent),
}

try:
    config_file = sys.argv[1]
    log.debug(f"Using specified config file: {config_file}")
except IndexError:
    config_file = os.path.join(DIR, "board", "config.json")

log.debug(f"config_file = {config_file}")

try:
    with open(config_file) as f:
        data = json.load(f)
except FileNotFoundError:
    log.debug(f"Using specified config file: {config_file}")
    data = {}

if sorted(data.keys()) != sorted(KEYS.keys()):
    log.warning("Existing config file has mismatched keys.")
    log.debug(data)
    data = {}

print("Configure:")
for k, v in KEYS.items():
    desc = v[0]
    cast = v[1]
    current = data.get(k)
    print(f"{k} ({desc})")
    if current is not None:
        print(f"[{current}]", end="")
    print(": ", end="")
    inp = input()
    if inp == "" and current:
        inp = current
        print(f"(used {current})")

    data[k] = cast(inp)

cfg = json.dumps(data, indent=2)
print("Configuration:")
print(cfg)

with open(config_file, "w") as f:
    f.write(cfg)

log.info(f"Wrote file {config_file}")
