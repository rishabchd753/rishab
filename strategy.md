# ETH Intraday Trend-Pullback Strategy (15m)

A fully mechanical day-trading strategy for ETH/USDT on 15-minute candles.
Every rule is exact so it can be backtested and judged on numbers, not vibes.

## Why this design

- **Trend-following** is the most robust documented edge in crypto. Win rate
  will be modest (~35–45%); profitability comes from winners being ~2x losers.
- **Pullback entries** (instead of chasing breakouts) improve the entry price
  and tighten the stop, which improves reward:risk.
- **A regime filter** keeps you out of counter-trend trades, which is where
  most intraday systems bleed.
- **A time stop** makes it a *day* strategy: positions don't linger overnight
  into news you never planned for.

## Rules

### Regime filter (higher-timeframe trend)
- Compute EMA(200) on the 15m closes (≈ 50 hours of price).
- Price above EMA(200) → **long trades only**.
- Price below EMA(200) → **short trades only** (or flat if `--long-only`).

### Long entry (mirror for shorts)
1. Momentum aligned: EMA(9) > EMA(21).
2. Pullback: the bar's **low touches or pierces EMA(21)**.
3. Reclaim: the same bar **closes back above EMA(21)**.
4. Enter at the **next bar's open** (no look-ahead).

### Exits (first one hit wins)
- **Stop loss:** entry − 1.5 × ATR(14) (intrabar, checked against the low).
- **Take profit:** entry + 2 × (entry − stop) — i.e. a fixed 2R target.
- **Time stop:** close at the open of the 24th bar after entry (6 hours) if
  neither level was hit. Day traders don't hold stale positions.

If a single bar's range covers both the stop and the target, the backtest
assumes the **stop fired first** (pessimistic, the honest choice).

### Position sizing
- Risk a fixed fraction of current equity per trade (default **1%**).
- Size = (equity × risk%) / (entry − stop). Never more than that.

### Costs
- Fee: 0.05% per side (Binance taker) — configurable.
- Slippage: 0.02% per side — configurable.
- Costs are applied to every entry and every exit. A strategy that only works
  at zero fees is not a strategy.

## How to judge the results

- **Expectancy per trade** (after costs) must be positive.
- **Profit factor** > 1.3 across several years is respectable for intraday.
- **Max drawdown** tells you if you could psychologically survive it.
- Check the **out-of-sample split**: the backtest reports the last 25% of the
  period separately. If the strategy only works in-sample, it's curve-fit.
- Expect losing streaks of 6–10 trades at a ~40% win rate. That's normal.

## What this is not

No backtest guarantees future returns. Crypto regimes change. This repo gives
you a measured, honest starting point — not a money printer.
