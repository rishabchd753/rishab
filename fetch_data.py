#!/usr/bin/env python3
"""Download historical ETH/USDT 15m candles from Binance's public API.

No API key required. Run this on your own machine (some sandboxes block
exchange APIs), then point backtest.py at the CSV it writes.

Usage:
    python fetch_data.py --years 3
    python fetch_data.py --symbol ETHUSDT --interval 15m --years 2 --out data/eth_15m.csv
"""

import argparse
import csv
import sys
import time
from datetime import datetime, timedelta, timezone

import requests

BASE_URL = "https://api.binance.com/api/v3/klines"
FALLBACK_URL = "https://data-api.binance.vision/api/v3/klines"
MAX_LIMIT = 1000

COLUMNS = ["timestamp", "open", "high", "low", "close", "volume"]


def fetch_klines(symbol: str, interval: str, start_ms: int, end_ms: int, url: str):
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_ms,
        "endTime": end_ms,
        "limit": MAX_LIMIT,
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--symbol", default="ETHUSDT")
    parser.add_argument("--interval", default="15m")
    parser.add_argument("--years", type=float, default=3.0, help="How many years of history")
    parser.add_argument("--out", default="data/eth_15m.csv")
    args = parser.parse_args()

    end = datetime.now(timezone.utc)
    start = end - timedelta(days=args.years * 365.25)
    start_ms = int(start.timestamp() * 1000)
    end_ms = int(end.timestamp() * 1000)

    url = BASE_URL
    rows = []
    cursor = start_ms
    print(f"Fetching {args.symbol} {args.interval} candles from {start:%Y-%m-%d} to {end:%Y-%m-%d} ...")

    while cursor < end_ms:
        try:
            batch = fetch_klines(args.symbol, args.interval, cursor, end_ms, url)
        except requests.RequestException as exc:
            if url == BASE_URL:
                print(f"  primary endpoint failed ({exc}); retrying via data-api.binance.vision")
                url = FALLBACK_URL
                continue
            raise
        if not batch:
            break
        for k in batch:
            # k = [openTime, open, high, low, close, volume, closeTime, ...]
            rows.append([
                datetime.fromtimestamp(k[0] / 1000, tz=timezone.utc).isoformat(),
                float(k[1]), float(k[2]), float(k[3]), float(k[4]), float(k[5]),
            ])
        cursor = batch[-1][0] + 1
        print(f"  {rows[-1][0]}  ({len(rows)} candles)", end="\r")
        time.sleep(0.15)  # stay well under Binance rate limits

    if not rows:
        print("No data returned — check symbol/interval.", file=sys.stderr)
        return 1

    import os
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)
        writer.writerows(rows)

    print(f"\nWrote {len(rows)} candles to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
