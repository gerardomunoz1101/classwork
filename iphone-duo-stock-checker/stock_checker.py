#!/usr/bin/env python3
"""Keep checking Apple Store stock for the iPhone Duo 256GB in Star White.

Polls Apple's public fulfillment endpoint (the one behind "Check availability"
on apple.com) every few minutes and alerts you the moment a store near you
has it for pickup, or online delivery opens up.

Only uses the Python standard library. Run with --help for options.
"""

import argparse
import http.cookiejar
import json
import platform
import random
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

# Apple part number for iPhone Duo 256GB Star White (US model).
# Other regions use different codes, e.g. MK2D4X/A (AU), MK2D4QN/A (EU).
DEFAULT_PART = "MK1E4LL/A"
DEFAULT_STORE_URL = "https://www.apple.com"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)


def log(msg):
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}", flush=True)


BROWSER_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9",
}


class AppleSession:
    """Talks to Apple like a browser would: visits the store first to pick up
    cookies, then reuses them for availability checks. Apple rejects bare
    requests without these (HTTP 541)."""

    def __init__(self, store_url):
        self.store_url = store_url
        self.cookies = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies))
        self.primed = False

    def prime(self):
        req = urllib.request.Request(f"{self.store_url}/shop/buy-iphone", headers={
            **BROWSER_HEADERS,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        })
        with self.opener.open(req, timeout=20) as resp:
            resp.read()
        self.primed = True

    def fetch_availability(self, part, zip_code):
        if not self.primed:
            self.prime()
        query = urllib.parse.urlencode({
            "fae": "true",
            "pl": "true",
            "mts.0": "regular",
            "mts.1": "compact",
            "parts.0": part,
            "searchNearby": "true",
            "location": zip_code,
        })
        req = urllib.request.Request(f"{self.store_url}/shop/fulfillment-messages?{query}", headers={
            **BROWSER_HEADERS,
            "Accept": "*/*",
            "Referer": f"{self.store_url}/shop/buy-iphone",
            "X-Requested-With": "XMLHttpRequest",
            "X-Aos-Ui-Fetch-Call-1": "true",
            "X-Skip-Redirect": "true",
        })
        try:
            with self.opener.open(req, timeout=20) as resp:
                return json.load(resp)
        except urllib.error.HTTPError:
            self.primed = False  # get fresh cookies on the next try
            raise


def parse_availability(data, part):
    """Return (stores_with_stock, delivery_text_or_None, stores_checked)."""
    content = data.get("body", {}).get("content", {})

    in_stock = []
    stores = content.get("pickupMessage", {}).get("stores", []) or []
    for store in stores:
        info = (store.get("partsAvailability") or {}).get(part) or {}
        if info.get("pickupDisplay") == "available":
            quote = info.get("pickupSearchQuote") or "Available"
            name = store.get("storeName", "Unknown store")
            city = store.get("city", "")
            in_stock.append(f"{name} ({city}): {quote}" if city else f"{name}: {quote}")

    delivery = None
    part_delivery = (content.get("deliveryMessage") or {}).get(part) or {}
    for mode in ("regular", "compact"):
        msg = part_delivery.get(mode) or {}
        if msg.get("isBuyable"):
            options = msg.get("deliveryOptionMessages") or []
            text = ", ".join(o.get("displayName", "") for o in options if o.get("displayName"))
            delivery = text or "Available to order online"
            break

    return in_stock, delivery, len(stores)


def notify(title, message, ntfy_topic):
    print("\a", end="", flush=True)  # terminal bell

    if ntfy_topic:
        # Free push notifications to your phone via the ntfy app (ntfy.sh).
        try:
            req = urllib.request.Request(
                f"https://ntfy.sh/{ntfy_topic}",
                data=message.encode(),
                headers={"Title": title, "Priority": "urgent", "Tags": "iphone"},
            )
            urllib.request.urlopen(req, timeout=15).close()
        except Exception as e:  # never let a failed alert kill the loop
            log(f"ntfy push failed: {e}")

    system = platform.system()
    try:
        if system == "Darwin":
            script = f"display notification {json.dumps(message)} with title {json.dumps(title)} sound name \"Glass\""
            subprocess.run(["osascript", "-e", script], check=False)
            subprocess.run(["say", title], check=False)
        elif system == "Linux":
            subprocess.run(["notify-send", "-u", "critical", title, message], check=False)
    except FileNotFoundError:
        pass


def main():
    p = argparse.ArgumentParser(description="Watch Apple Store stock for iPhone Duo 256GB Star White.")
    p.add_argument("--zip", required=True, help="ZIP / postal code to search near, e.g. 10001")
    p.add_argument("--part", default=DEFAULT_PART, help=f"Apple part number (default {DEFAULT_PART})")
    p.add_argument("--store-url", default=DEFAULT_STORE_URL,
                   help="Regional Apple site, e.g. https://www.apple.com/uk (default US)")
    p.add_argument("--interval", type=int, default=120,
                   help="Seconds between checks (default 120; don't go much lower or Apple may block you)")
    p.add_argument("--ntfy-topic", help="ntfy.sh topic name for phone push alerts")
    p.add_argument("--once", action="store_true", help="Check one time and exit")
    args = p.parse_args()

    log(f"Watching {args.part} (iPhone Duo 256GB Star White) near {args.zip}, every {args.interval}s. Ctrl+C to stop.")
    session = AppleSession(args.store_url.rstrip("/"))
    was_available = False
    failures = 0

    while True:
        try:
            data = session.fetch_availability(args.part, args.zip)
            in_stock, delivery, checked = parse_availability(data, args.part)
            failures = 0

            if in_stock or delivery:
                lines = [f"Pickup: {s}" for s in in_stock]
                if delivery:
                    lines.append(f"Delivery: {delivery}")
                message = "\n".join(lines)
                log("IN STOCK!\n  " + message.replace("\n", "\n  "))
                if not was_available:  # alert once per restock, not every poll
                    notify("iPhone Duo in stock!", message, args.ntfy_topic)
                was_available = True
            else:
                log(f"Not available ({checked} stores checked).")
                was_available = False
        except urllib.error.HTTPError as e:
            failures += 1
            body = e.read(300).decode(errors="replace").strip().replace("\n", " ")
            log(f"Apple returned HTTP {e.code} from {e.url.split('?')[0]}, retrying later. {body}")
        except Exception as e:
            failures += 1
            log(f"Check failed: {e}")

        if args.once:
            sys.exit(0 if was_available else 1)

        # Back off on repeated errors (up to 30 min), and add jitter so polls look less robotic.
        delay = min(args.interval * (2 ** min(failures, 4)), 1800) if failures else args.interval
        time.sleep(delay + random.uniform(0, 15))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
