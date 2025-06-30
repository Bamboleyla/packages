import pandas as pd


def manage_long(
    curr: pd.DataFrame,
    prev: pd.DataFrame,
    positions: int,
) -> (int, dict):
    """Управляет длинными позициями и возвращает новые позиции + сигнал."""

    is_open_time = (
        pd.to_datetime(curr.get("DATE")).time() > pd.Timestamp("09:30:00").time()
        and pd.to_datetime(curr.get("DATE")).time() < pd.Timestamp("23:40:00").time()
    )

    signal = None  # Инициализируем сигнал

    # Условие для открытия позиции
    if positions == 0 and is_open_time:
        if pd.notna(curr["PC_20_HIGH"]) and pd.notna(curr["ST_UPPER_30_7"]):
            if (
                curr["PC_20_HIGH"] < curr["ST_UPPER_30_7"]
                and curr["HIGH"] > prev["PC_20_HIGH"]
            ):
                positions += 1  # Увеличиваем позиции
                signal = {
                    "SIGNAL": "LONG_BUY",
                    "PRICE": prev["PC_20_HIGH"],
                    "COMMISSION": round(prev["PC_20_HIGH"] * 0.00005, 2),
                    "BALANCE": -prev["PC_20_HIGH"],
                }

    return positions, signal  # Возвращаем обновленные позиции и сигнал
