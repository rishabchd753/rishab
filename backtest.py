#!/usr/bin/env python3
"""Event-driven backtest for the ETH intraday trend-pullback strategy.

Usage:
    python backtest.py data/eth_15m.csv
    python backtest.py data/eth_15m.csv --equity 10000 --risk 0.01 --long-only

Reads a CSV produced by fetch_data.py (or any CSV with columns
timestamp,open,high,low,close,volume) and prints performance stats plus an
out-of-sample split. Writes trades.csv and equity_curve.csv next to the input.
"""

import argparse
import os

import numpy as np
import pandas as pd

import strategy as strat


def run_backtest(
    df: pd.DataFrame,
    starting_equity: float = 10_000.0,
    risk_pct: float = 0.01,
    fee_pct: float = 0.0005,
    slippage_pct: float = 0.0002,
    long_only: bool = False,
):
    data = strat.generate_signals(df, long_only=long_only).reset_index(drop=True)

    equity = starting_equity
    trades = []
    equity_curve = []

    in_pos = False
    direction = 0
    entry_price = stop = target = qty = 0.0
    entry_time = None
    entry_bar = 0
    cost_per_side = fee_pct + slippage_pct

    for i in range(1, len(data)):
        bar = data.iloc[i]

        if in_pos:
            exit_price = None
            reason = None
            if direction == 1:
                # Pessimistic: if both stop and target are inside the bar,
                # assume the stop was hit first.
                if bar["low"] <= stop:
                    exit_price, reason = stop, "stop"
                elif bar["high"] >= target:
                    exit_price, reason = target, "target"
            else:
                if bar["high"] >= stop:
                    exit_price, reason = stop, "stop"
                elif bar["low"] <= target:
                    exit_price, reason = target, "target"
            if exit_price is None and i - entry_bar >= strat.MAX_HOLD_BARS:
                exit_price, reason = bar["open"], "time"

            if exit_price is not None:
                gross = direction * (exit_price - entry_price) * qty
                costs = (entry_price + exit_price) * qty * cost_per_side
                pnl = gross - costs
                equity += pnl
                trades.append(
                    {
                        "entry_time": entry_time,
                        "exit_time": bar["timestamp"],
                        "direction": "long" if direction == 1 else "short",
                        "entry": round(entry_price, 2),
                        "exit": round(exit_price, 2),
                        "reason": reason,
                        "pnl": round(pnl, 2),
                        "equity_after": round(equity, 2),
                    }
                )
                in_pos = False

        if not in_pos:
            prev = data.iloc[i - 1]
            if prev["signal"] != 0 and not np.isnan(prev["atr"]):
                direction = int(prev["signal"])
                entry_price = bar["open"]
                stop, target = strat.stop_and_target(entry_price, direction, prev["atr"])
                risk_per_unit = abs(entry_price - stop)
                if risk_per_unit > 0 and equity > 0:
                    qty = (equity * risk_pct) / risk_per_unit
                    entry_time = bar["timestamp"]
                    entry_bar = i
                    in_pos = True

        equity_curve.append({"timestamp": bar["timestamp"], "equity": equity})

    return pd.DataFrame(trades), pd.DataFrame(equity_curve)


def summarize(trades: pd.DataFrame, curve: pd.DataFrame, starting_equity: float, label: str) -> str:
    lines = [f"--- {label} ---"]
    if trades.empty:
        lines.append("No trades.")
        return "\n".join(lines)

    wins = trades[trades["pnl"] > 0]
    losses = trades[trades["pnl"] <= 0]
    win_rate = len(wins) / len(trades)
    gross_win = wins["pnl"].sum()
    gross_loss = -losses["pnl"].sum()
    profit_factor = gross_win / gross_loss if gross_loss > 0 else float("inf")
    expectancy = trades["pnl"].mean()

    eq = curve["equity"]
    peak = eq.cummax()
    max_dd = ((eq - peak) / peak).min()
    total_return = eq.iloc[-1] / starting_equity - 1

    lines += [
        f"Trades:            {len(trades)}",
        f"Win rate:          {win_rate:.1%}",
        f"Profit factor:     {profit_factor:.2f}",
        f"Expectancy/trade:  ${expectancy:,.2f}",
        f"Avg win / loss:    ${wins['pnl'].mean():,.2f} / ${losses['pnl'].mean():,.2f}",
        f"Total return:      {total_return:.1%}",
        f"Max drawdown:      {max_dd:.1%}",
        f"Final equity:      ${eq.iloc[-1]:,.2f}",
        "Exits: " + ", ".join(f"{k}={v}" for k, v in trades["reason"].value_counts().items()),
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", help="Candle CSV from fetch_data.py")
    parser.add_argument("--equity", type=float, default=10_000.0)
    parser.add_argument("--risk", type=float, default=0.01, help="Risk per trade as a fraction of equity")
    parser.add_argument("--fee", type=float, default=0.0005, help="Fee per side (0.0005 = 0.05%%)")
    parser.add_argument("--slippage", type=float, default=0.0002)
    parser.add_argument("--long-only", action="store_true")
    args = parser.parse_args()

    df = pd.read_csv(args.csv, parse_dates=["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    print(f"Loaded {len(df)} candles: {df['timestamp'].iloc[0]} → {df['timestamp'].iloc[-1]}")

    trades, curve = run_backtest(
        df,
        starting_equity=args.equity,
        risk_pct=args.risk,
        fee_pct=args.fee,
        slippage_pct=args.slippage,
        long_only=args.long_only,
    )

    print()
    print(summarize(trades, curve, args.equity, "FULL PERIOD"))

    # Out-of-sample check: rerun on the last 25% of candles only, so the
    # holdout has its own equity base and the split is honest.
    split = int(len(df) * 0.75)
    oos_trades, oos_curve = run_backtest(
        df.iloc[split:].reset_index(drop=True),
        starting_equity=args.equity,
        risk_pct=args.risk,
        fee_pct=args.fee,
        slippage_pct=args.slippage,
        long_only=args.long_only,
    )
    print()
    print(summarize(oos_trades, oos_curve, args.equity, "OUT-OF-SAMPLE (last 25% of candles)"))

    out_dir = os.path.dirname(os.path.abspath(args.csv))
    trades.to_csv(os.path.join(out_dir, "trades.csv"), index=False)
    curve.to_csv(os.path.join(out_dir, "equity_curve.csv"), index=False)
    print(f"\nWrote trades.csv and equity_curve.csv to {out_dir}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
