# ETH Day-Trading Strategy Backtester

A fully mechanical, backtestable intraday strategy for ETH/USDT on 15-minute
candles: trend-pullback entries with ATR stops, a 2R target, a 6-hour time
stop, 1%-risk position sizing, and realistic fees/slippage.

The exact rules (and how to judge the results honestly) are in
[strategy.md](strategy.md).

## Quick start

```bash
pip install -r requirements.txt

# 1. Download real ETH/USDT 15m history from Binance (no API key needed).
#    Run this on your own machine — some sandboxes block exchange APIs.
python fetch_data.py --years 3

# 2. Run the backtest.
python backtest.py data/eth_15m.csv
```

Useful flags:

```bash
python backtest.py data/eth_15m.csv --long-only          # skip shorts
python backtest.py data/eth_15m.csv --risk 0.005         # risk 0.5%/trade
python backtest.py data/eth_15m.csv --fee 0.001          # stress-test fees
```

The report prints full-period stats **and an out-of-sample split** (the last
25% of candles, run with a fresh equity base). It also writes `trades.csv`
(every trade with entry/exit/reason) and `equity_curve.csv` next to your data
file so you can inspect or plot everything.

## No internet? Smoke-test the pipeline

```bash
python make_demo_data.py
python backtest.py data/eth_15m_DEMO.csv
```

The demo data is synthetic. It proves the code runs; it says **nothing**
about real profitability.

## Files

| File | Purpose |
| --- | --- |
| `strategy.md` | Exact strategy rules and how to evaluate results |
| `fetch_data.py` | Downloads historical candles from Binance public API |
| `strategy.py` | Indicator + signal logic (no look-ahead) |
| `backtest.py` | Event-driven backtest engine, stats, OOS split |
| `make_demo_data.py` | Synthetic data generator for smoke tests |
| `eth_trend_pullback.pine` | The trend strategy as a TradingView Pine Script |
| `eth_range_reversion.pine` | Mean-reversion strategy for ranging (ADX < 25) markets |

## Backtesting on TradingView

Paste either `.pine` file into TradingView's Pine Editor on an ETHUSDT 15m
chart and open the Strategy Tester tab. Same fees and sizing as the Python
engine.

The two scripts are regime complements:

- **Trend-pullback** trades only when ADX ≥ 20 and price is away from the
  EMA(200). It profits in trending markets and (by design) sits out chop.
- **Range-reversion** trades only when ADX ≤ 25. It fades Bollinger-band
  extremes back to the middle of the range and profits in sideways markets —
  exactly where the trend strategy bleeds.

Test both over the same period: whichever regime dominates decides which
strategy carried it. Neither wins in both regimes; that's why there are two.

## Honest disclaimers

- Backtest results are not future returns. Crypto regimes change.
- The engine is deliberately pessimistic: entries at next-bar open, stop
  assumed to fire before target when both are inside one bar, costs on every
  side of every trade.
- If it only profits in-sample or only at zero fees, don't trade it.
- Never trade money you can't afford to lose. This is research tooling, not
  financial advice.
