# __init__.py
from myLib.brokers import BrokerAbstractClass
from .methods.plot_data import plot_data
from ..strategy import StrategyAbstractClass
import pandas as pd
import numpy as np

__all__ = ["PriceChanelGrid"]


class PriceChanelGrid(StrategyAbstractClass):
    def __init__(self, broker: BrokerAbstractClass) -> None:
        super().__init__()
        self.name: str = "PriceChanelGrid"
        self._broker: BrokerAbstractClass = broker
        self._config = {
            "indicators": [
                {"type": "price_chanel", "period": 20},
                {"type": "super_trend", "period": 30, "multiplier": 7},
            ]
        }

    def run(self, data: pd.DataFrame) -> pd.DataFrame:
        # Векторизованные вычисления времени
        data["DATE"] = pd.to_datetime(data["DATE"])
        times = data["DATE"].dt.time
        open_time = pd.Timestamp("09:30:00").time()
        close_time = pd.Timestamp("23:40:00").time()

        # Предварительный расчет всех условий
        data["prev_PC_20_HIGH"] = data["PC_20_HIGH"].shift(1)
        data["open_condition"] = (
            data["PC_20_HIGH"].notna()
            & data["ST_UPPER_30_7"].notna()
            & (data["PC_20_HIGH"] < data["ST_UPPER_30_7"])
            & (data["HIGH"] > data["prev_PC_20_HIGH"])
        )

        # Инициализация колонок
        data["SIGNAL"] = np.nan
        data["BUY_PRICE"] = np.nan
        data["SELL_PRICE"] = np.nan
        data["COMMISSION"] = np.nan
        data["BALANCE"] = np.nan

        # Векторизованное определение потенциальных сигналов
        buy_mask = (times > open_time) & (times < close_time) & data["open_condition"]
        close_time_mask = times == close_time

        # Создаем список всех событий (открытий и закрытий)
        events = []

        # Добавляем события открытия
        for idx in data.index[buy_mask]:
            events.append(
                {"index": idx, "type": "BUY", "price": data.loc[idx, "prev_PC_20_HIGH"]}
            )

        # Добавляем события закрытия по времени
        for idx in data.index[close_time_mask]:
            events.append(
                {"index": idx, "type": "CLOSE_TIME", "price": data.loc[idx, "CLOSE"]}
            )

        # Добавляем событие закрытия в конце данных
        last_idx = data.index[-1]
        events.append(
            {
                "index": last_idx,
                "type": "CLOSE_END",
                "price": data.loc[last_idx, "CLOSE"],
            }
        )

        # Сортируем события по времени (индексу)
        events.sort(key=lambda x: x["index"])

        # Обрабатываем события с отслеживанием позиции
        position_open = False
        open_index = None

        for event in events:
            idx = event["index"]

            # Обработка открытия
            if event["type"] == "BUY" and not position_open:
                position_open = True
                open_index = idx
                data.loc[idx, "SIGNAL"] = "LONG_BUY"
                data.loc[idx, "BUY_PRICE"] = event["price"]
                data.loc[idx, "COMMISSION"] = round(event["price"] * 0.00005, 2)
                data.loc[idx, "BALANCE"] = -event["price"]

            # Обработка закрытия при открытой позиции
            elif event["type"] in ["CLOSE_TIME", "CLOSE_END"] and position_open:
                position_open = False
                data.loc[idx, "SIGNAL"] = "LONG_SELL"
                data.loc[idx, "SELL_PRICE"] = event["price"]
                data.loc[idx, "COMMISSION"] = round(event["price"] * 0.00005, 2)
                data.loc[idx, "BALANCE"] = event["price"]

                # Удаляем событие закрытия в конце, если оно уже обработано как закрытие по времени
                if event["type"] == "CLOSE_TIME" and idx == last_idx:
                    data.drop(last_idx, inplace=True, errors="ignore")

        return data

    def get_config(self) -> dict:
        return self._config

    def get_plot_data(self):
        return plot_data()
