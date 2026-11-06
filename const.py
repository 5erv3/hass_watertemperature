"""Constants for the GKD Bayern Wassertemperatur integration."""
DOMAIN = "gkd_wassertemperatur"

CONF_URL = "url"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_NAME = "Wassertemperatur Ammersee"
DEFAULT_URL = (
    "https://www.gkd.bayern.de/de/seen/wassertemperatur/isar/"
    "stegen-16602008/messwerte/tabelle"
)
DEFAULT_SCAN_INTERVAL = 30  # Minuten
MIN_SCAN_INTERVAL = 10
MAX_SCAN_INTERVAL = 1440

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
    "Referer": "https://www.gkd.bayern.de/",
}
