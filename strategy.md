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

### Chop filters (v2) — "no trade" is a position
A trend strategy in a flat market overtrades and bleeds fees: price hugs the
EMAs, so the pullback condition fires nearly every bar. Three gates keep the
strategy out of chop:
1. **Trend strength:** ADX(14) must be ≥ 20. Below that, the market is
   officially going nowhere — no trades in either direction.
2. **Regime distance:** price must be at least 0.5 × ATR(14) away from the
   EMA(200). If price is sitting on the regime line, there is no regime.
3. **Cooldown:** after any exit, wait 12 bars (3 hours) before the next
   entry. Prevents machine-gun re-entries into the same dead range.
4. **Volatility floor (v3):** ATR(14) must be at least 0.15% of price.
   Round-trip costs are ~0.14% of the position; if the typical bar move is
   smaller than that, every exit — even the winners — loses to fees. This is
   the rule that keeps both strategies flat in dead, compressed markets like
   ETH pinned at $1,800: the expected move must pay for the trade several
   times over, or there is no trade. (The range-reversion Pine script uses
   the equivalent gate: minimum Bollinger band width of 0.6% of price, since
   its profit target is the middle band.)

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
