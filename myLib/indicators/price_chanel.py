import pandas as pd


def price_chanel(df: pd.DataFrame, period: int) -> pd.DataFrame:
    result_df = df.copy()

    result_df[f"PC {period} HIGH"] = result_df["HIGH"].rolling(window=period).max()
    result_df[f"PC {period} LOW"] = result_df["LOW"].rolling(window=period).min()
    result_df[f"PC {period} MID"] = round(
        (result_df[f"PC {period} HIGH"] + result_df[f"PC {period} LOW"]) / 2, 2
    )

    return result_df
