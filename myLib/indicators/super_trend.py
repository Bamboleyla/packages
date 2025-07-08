import pandas as pd
import talib
import numpy as np


def super_trend(df: pd.DataFrame, config: list) -> pd.DataFrame:
    """
    Calculates the SuperTrend indicator for multiple configurations.

    Parameters:
        df: DataFrame with columns ['OPEN', 'HIGH', 'LOW', 'CLOSE']
        config: List of dictionaries with indicator parameters [{'period': int, 'multiplier': int}]

    Returns:
        New DataFrame with added columns for each configuration
    """
    # Create a copy of DataFrame for safe column addition
    df = df.copy()

    # For each configuration in the list
    for params in config:
        period = params["period"]
        multiplier = params["multiplier"]

        # Calculate ATR
        atr = talib.ATR(df["HIGH"], df["LOW"], df["CLOSE"], timeperiod=period)

        # Basic lines
        hl2 = (df["HIGH"] + df["LOW"]) / 2
        basic_upper = hl2 + multiplier * atr
        basic_lower = hl2 - multiplier * atr

        # Initialize result arrays
        n = len(df)
        st_upper = np.full(n, np.nan)
        st_lower = np.full(n, np.nan)
        trend = np.zeros(n, dtype=int)  # 1 = upper trend, -1 = lower trend

        # First index with valid ATR
        start_idx = period
        if start_idx >= n:
            # Add empty columns if not enough data
            df[f"ST_UPPER_{period}_{multiplier}"] = np.nan
            df[f"ST_LOWER_{period}_{multiplier}"] = np.nan
            continue

        # Convert to numpy arrays for speed
        close_arr = df["CLOSE"].values
        basic_upper_arr = basic_upper.values
        basic_lower_arr = basic_lower.values

        # Initialize first value (start with lower trend)
        st_upper[start_idx] = basic_upper_arr[start_idx]
        st_lower[start_idx] = basic_lower_arr[start_idx]
        trend[start_idx] = 1  # Start with lower trend

        # Main calculation loop
        for i in range(start_idx + 1, n):
            # Skip NaN values
            if np.isnan(basic_upper_arr[i]) or np.isnan(basic_lower_arr[i]):
                continue

            # Calculate lines BASED ON PREVIOUS TREND
            if trend[i - 1] == 1:  # Previous trend was upper
                st_upper[i] = min(basic_upper_arr[i], st_upper[i - 1])
                st_lower[i] = basic_lower_arr[i]
            else:  # Previous trend was lower
                st_upper[i] = basic_upper_arr[i]
                st_lower[i] = max(basic_lower_arr[i], st_lower[i - 1])

            # Determine current trend BASED ON CURRENT CANDLE CLOSE
            if trend[i - 1] == 1 and close_arr[i] > st_upper[i]:
                trend[i] = -1  # Switch to upper trend
            elif trend[i - 1] == -1 and close_arr[i] < st_lower[i]:
                trend[i] = 1  # Switch to lower trend
            else:
                trend[i] = trend[i - 1]  # Keep previous trend

        # Round values to 3 decimal places
        st_upper = np.round(st_upper, 3)
        st_lower = np.round(st_lower, 3)

        # Create columns based on current trend
        upper_col = np.where(trend == 1, st_upper, np.nan)
        lower_col = np.where(trend == -1, st_lower, np.nan)

        # Add results to DataFrame
        df[f"ST_UPPER_{period}_{multiplier}"] = upper_col
        df[f"ST_LOWER_{period}_{multiplier}"] = lower_col

    return df
