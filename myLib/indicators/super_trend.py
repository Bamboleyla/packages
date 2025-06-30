import pandas as pd
import talib
import numpy as np


def super_trend(df: pd.DataFrame, config: list) -> pd.DataFrame:
    """
    Рассчитывает индикатор SuperTrend для нескольких конфигураций.

    Параметры:
        df: DataFrame с колонками ['OPEN', 'HIGH', 'LOW', 'CLOSE']
        config: Список словарей с параметрами индикатора [{'period': int, 'multiplier': int}]

    Возвращает:
        Новый DataFrame с добавленными колонками для каждой конфигурации
    """
    # Создаем копию DataFrame для безопасного добавления колонок
    df = df.copy()

    # Для каждой конфигурации в списке
    for params in config:
        period = params["period"]
        multiplier = params["multiplier"]

        # Рассчитываем ATR
        atr = talib.ATR(df["HIGH"], df["LOW"], df["CLOSE"], timeperiod=period)

        # Базовые линии (классический метод)
        hl2 = (df["HIGH"] + df["LOW"]) / 2
        basic_upper = hl2 + multiplier * atr
        basic_lower = hl2 - multiplier * atr

        # Инициализация массивов для результатов
        n = len(df)
        st_upper = np.full(n, np.nan)
        st_lower = np.full(n, np.nan)
        trend = np.zeros(n, dtype=int)  # 1 = верхний тренд, -1 = нижний тренд

        # Первый индекс с валидным ATR
        start_idx = period
        if start_idx >= n:
            # Добавляем пустые колонки если данных недостаточно
            df[f"ST_UPPER_{period}_{multiplier}"] = np.nan
            df[f"ST_LOWER_{period}_{multiplier}"] = np.nan
            continue

        # Конвертируем в numpy массивы для ускорения
        close_arr = df["CLOSE"].values
        basic_upper_arr = basic_upper.values
        basic_lower_arr = basic_lower.values

        # Инициализация первого значения (начинаем с нижнего тренда)
        st_upper[start_idx] = basic_upper_arr[start_idx]
        st_lower[start_idx] = basic_lower_arr[start_idx]
        trend[start_idx] = -1  # Начинаем с нижнего тренда

        # Основной цикл расчета
        for i in range(start_idx + 1, n):
            # Пропускаем NaN значения
            if np.isnan(basic_upper_arr[i]) or np.isnan(basic_lower_arr[i]):
                continue

            # Рассчитываем линии ИСХОДЯ ИЗ ПРЕДЫДУЩЕГО ТРЕНДА
            if trend[i - 1] == 1:  # Предыдущий тренд был верхний
                st_upper[i] = min(basic_upper_arr[i], st_upper[i - 1])
                st_lower[i] = basic_lower_arr[i]
            else:  # Предыдущий тренд был нижний
                st_upper[i] = basic_upper_arr[i]
                st_lower[i] = max(basic_lower_arr[i], st_lower[i - 1])

            # Определяем текущий тренд ПО ЗАКРЫТИЮ ТЕКУЩЕЙ СВЕЧИ
            if trend[i - 1] == 1 and close_arr[i] > st_upper[i]:
                trend[i] = -1  # Переход в верхний тренд
            elif trend[i - 1] == -1 and close_arr[i] < st_lower[i]:
                trend[i] = 1  # Переход в нижний тренд
            else:
                trend[i] = trend[i - 1]  # Сохраняем предыдущий тренд

        # Округляем значения до 3 знаков
        st_upper = np.round(st_upper, 3)
        st_lower = np.round(st_lower, 3)

        # Создаем колонки с учетом текущего тренда
        upper_col = np.where(trend == 1, st_upper, np.nan)
        lower_col = np.where(trend == -1, st_lower, np.nan)

        # Добавляем результаты в DataFrame
        df[f"ST_UPPER_{period}_{multiplier}"] = upper_col
        df[f"ST_LOWER_{period}_{multiplier}"] = lower_col

    return df
