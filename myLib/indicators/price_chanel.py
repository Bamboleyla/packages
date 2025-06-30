import pandas as pd


def price_chanel(df: pd.DataFrame, period: int) -> pd.DataFrame:
    result_df = df.copy()

    result_df[f"PC_{period}_HIGH"] = result_df["HIGH"].rolling(window=period).max()
    result_df[f"PC_{period}_LOW"] = result_df["LOW"].rolling(window=period).min()
    result_df[f"PC_{period}_MID"] = round(
        (result_df[f"PC_{period}_HIGH"] + result_df[f"PC_{period}_LOW"]) / 2, 2
    )

    return result_df
