#!/usr/bin/env python3
"""Generate SYNTHETIC ETH-like 15m candles to smoke-test the pipeline.

THIS IS NOT REAL MARKET DATA. Results on it say nothing about real
profitability — it exists only to verify that fetch → signals → backtest →
reports all run. For real results, run fetch_data.py on your machine.
"""

import argparse
import os

import numpy as np
import pandas as pd


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=365)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--out", default="data/eth_15m_DEMO.csv")
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    n = args.days * 96  # 96 fifteen-minute bars per day

    # Regime-switching geometric random walk: alternating drift regimes with
    # volatility clustering, loosely calibrated to ETH 15m behaviour.
    regime_len = rng.integers(96 * 5, 96 * 30, size=200)
    drifts = rng.choice([-0.00004, 0.0, 0.00005], size=200, p=[0.3, 0.3, 0.4])
    drift = np.repeat(drifts, regime_len)[:n]

    vol = np.zeros(n)
    vol[0] = 0.003
    shocks = rng.standard_normal(n)
    for i in range(1, n):  # GARCH-ish volatility clustering
        vol[i] = np.sqrt(0.0000002 + 0.12 * (vol[i - 1] * shocks[i - 1]) ** 2 + 0.86 * vol[i - 1] ** 2)
    rets = drift + vol * shocks

    close = 2500.0 * np.exp(np.cumsum(rets))
    open_ = np.empty(n)
    open_[0] = close[0]
    open_[1:] = close[:-1]
    wick = np.abs(rng.standard_normal(n)) * vol * close
    high = np.maximum(open_, close) + wick
    low = np.minimum(open_, close) - np.abs(rng.standard_normal(n)) * vol * close
    volume = rng.lognormal(6, 1, n)

    ts = pd.date_range("2025-01-01", periods=n, freq="15min", tz="UTC")
    df = pd.DataFrame(
        {"timestamp": ts, "open": open_, "high": high, "low": low, "close": close, "volume": volume}
    )

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    df.to_csv(args.out, index=False)
    print(f"Wrote {n} SYNTHETIC candles to {args.out} (demo only — not real ETH data)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
