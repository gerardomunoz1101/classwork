# iPhone Duo stock checker

Keeps checking Apple Store availability for the **iPhone Duo 256GB in Star White**
and alerts you when it shows up for in-store pickup near you or for online delivery.

Needs only Python 3, with nothing to install.

## Run it

```sh
python3 stock_checker.py --zip 10001
```

It checks every 2 minutes until you press Ctrl+C. When the phone comes in stock it:

- prints the stores that have it,
- rings the terminal bell,
- shows a desktop notification (macOS also says it out loud),
- sends a push to your iPhone if you set `--ntfy-topic` (see below).

You get one alert each time it comes back in stock, not one on every check.

## Push alerts to your phone

1. Install the free **ntfy** app from the App Store.
2. Subscribe to a topic name nobody else would guess, e.g. `gerardo-iphone-duo-8213`.
3. Run:

```sh
python3 stock_checker.py --zip 10001 --ntfy-topic gerardo-iphone-duo-8213
```

## Options

| Option | Default | Meaning |
| --- | --- | --- |
| `--zip` | (required) | ZIP/postal code to search near |
| `--interval` | `120` | Seconds between checks. Going much lower risks Apple blocking you. |
| `--part` | `MK1E4LL/A` | Apple part number (US Star White 256GB) |
| `--store-url` | `https://www.apple.com` | Regional store, e.g. `https://www.apple.com/uk` |
| `--ntfy-topic` | none | ntfy.sh topic for phone push alerts |
| `--once` | off | Check once and exit (exit code 0 = in stock) |

Outside the US, pass your region's part number. Retailer listings show
`MK2D4X/A` (Australia) and `MK2D4QN/A` (EU). You can confirm yours in the URL
or page source of the Apple Store product page.

## Keep it running in the background

macOS/Linux:

```sh
nohup python3 stock_checker.py --zip 10001 --ntfy-topic YOUR_TOPIC > stock.log 2>&1 &
```

Your computer has to stay awake for checks to keep happening.
