"""Signal logic for the ETH intraday trend-pullback strategy.

Pure functions over a pandas DataFrame with columns:
timestamp, open, high, low, close, volume.

All indicators are computed on closed bars only; entries execute on the NEXT
bar's open, so there is no look-ahead bias.
"""

import numpy as np
import pandas as pd

# Strategy parameters (exact rules documented in strategy.md)
EMA_FAST = 9
EMA_SLOW = 21
EMA_REGIME = 200
ATR_PERIOD = 14
ATR_STOP_MULT = 1.5
REWARD_RISK = 2.0
MAX_HOLD_BARS = 24  # 6 hours on 15m candles

# v2 chop filters: a trend strategy must sit out trendless markets, otherwise
# it overtrades sideways price and bleeds fees (see strategy.md).
ADX_PERIOD = 14
ADX_MIN = 20.0            # no trades unless the market is actually trending
REGIME_DIST_ATR = 0.5     # price must be at least this many ATRs from EMA(200)
COOLDOWN_BARS = 12        # 3h pause after an exit before the next entry


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def atr(df: pd.DataFrame, period: int = ATR_PERIOD) -> pd.Series:
    prev_close = df["close"].shift(1)
    tr = pd.concat(
        [
            df["high"] - df["low"],
            (df["high"] - prev_close).abs(),
            (df["low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return tr.ewm(alpha=1 / period, adjust=False).mean()


def adx(df: pd.DataFrame, period: int = ADX_PERIOD) -> pd.Series:
    """Wilder's ADX — measures trend strength regardless of direction."""
    up = df["high"].diff()
    down = -df["low"].diff()
    plus_dm = pd.Series(np.where((up > down) & (up > 0), up, 0.0), index=df.index)
    minus_dm = pd.Series(np.where((down > up) & (down > 0), down, 0.0), index=df.index)

    prev_close = df["close"].shift(1)
    tr = pd.concat(
        [
            df["high"] - df["low"],
            (df["high"] - prev_close).abs(),
            (df["low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)

    alpha = 1 / period
    atr_w = tr.ewm(alpha=alpha, adjust=False).mean()
    plus_di = 100 * plus_dm.ewm(alpha=alpha, adjust=False).mean() / atr_w
    minus_di = 100 * minus_dm.ewm(alpha=alpha, adjust=False).mean() / atr_w
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
    return dx.ewm(alpha=alpha, adjust=False).mean()


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ema_fast"] = ema(out["close"], EMA_FAST)
    out["ema_slow"] = ema(out["close"], EMA_SLOW)
    out["ema_regime"] = ema(out["close"], EMA_REGIME)
    out["atr"] = atr(out)
    out["adx"] = adx(out)
    return out


def generate_signals(df: pd.DataFrame, long_only: bool = False) -> pd.DataFrame:
    """Mark bars whose close completes an entry setup.

    signal = +1 → go long at next bar's open
    signal = -1 → go short at next bar's open
    """
    out = add_indicators(df)

    # Chop filters: require real trend strength AND real distance from the
    # regime EMA. In flat markets price hugs every EMA, so without these two
    # gates the pullback condition fires almost every bar.
    trending = out["adx"] >= ADX_MIN
    regime_dist = (out["close"] - out["ema_regime"]).abs() >= REGIME_DIST_ATR * out["atr"]

    uptrend = (out["close"] > out["ema_regime"]) & trending & regime_dist
    downtrend = (out["close"] < out["ema_regime"]) & trending & regime_dist
    momentum_up = out["ema_fast"] > out["ema_slow"]
    momentum_down = out["ema_fast"] < out["ema_slow"]

    long_setup = (
        uptrend
        & momentum_up
        & (out["low"] <= out["ema_slow"])   # pullback touched EMA(21)
        & (out["close"] > out["ema_slow"])  # ...and closed back above it
    )
    short_setup = (
        downtrend
        & momentum_down
        & (out["high"] >= out["ema_slow"])
        & (out["close"] < out["ema_slow"])
    )

    out["signal"] = 0
    out.loc[long_setup, "signal"] = 1
    if not long_only:
        out.loc[short_setup, "signal"] = -1

    # Indicators need warm-up: suppress signals before the regime EMA is real.
    out.loc[: out.index[min(EMA_REGIME, len(out) - 1)], "signal"] = 0
    out["signal"] = out["signal"].where(~(out["atr"].isna() | out["adx"].isna()), 0)
    return out


def stop_and_target(entry: float, direction: int, atr_value: float):
    risk = ATR_STOP_MULT * atr_value
    stop = entry - direction * risk
    target = entry + direction * REWARD_RISK * risk
    return stop, target
