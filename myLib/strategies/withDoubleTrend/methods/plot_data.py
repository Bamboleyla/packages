from myLib.strategies.withDoubleTrend.types import DoubleTrendSignals


def plot_data():
    return {
        "legend": "WithDoubleTrend",
        "required_columns": [
            "OPEN",
            "CLOSE",
            "HIGH",
            "LOW",
            "DATE",
            "SIGNAL",
            "TAKE_PROFIT",
            "BUY_PRICE",
            "SELL_PRICE",
            "ST 10 3 UP",
            "ST 10 3 LOW",
            "ST 20 5 UP",
            "ST 20 5 LOW",
        ],
        "plots": [
            {"column": "ST 10 3 UP", "color": "#FF0000", "width": 2},
            {"column": "ST 10 3 LOW", "color": "#228B22", "width": 2},
            {"column": "ST 20 5 UP", "color": "#B22222", "width": 3},
            {"column": "ST 20 5 LOW", "color": "#006400", "width": 3},
            {"column": "EMA 50", "color": "#3C74BD", "width": 1},
            {"column": "TAKE_PROFIT", "color": "#47F77B", "width": 1},
        ],
        "actions": [
            {"column": "BUY_PRICE", "color": "#000000", "style": "x", "width": 2},
            {"column": "SELL_PRICE", "color": "#000000", "style": "x", "width": 2},
        ],
        "signals": [
            {
                "name": DoubleTrendSignals.LONG_BUY,
                "price_col": "BUY_PRICE",
                "offset": -1,
                "color": "#4a6",
                "style": "^",
                "legend": "buy",
                "width": 2,
            },
            {
                "name": DoubleTrendSignals.LONG_SELL,
                "price_col": "SELL_PRICE",
                "offset": 1,
                "color": "#4a6",
                "style": "o",
                "legend": "sell",
                "width": 2,
            },
            {
                "name": DoubleTrendSignals.LONG_TP,
                "price_col": "TAKE_PROFIT",
                "offset": 1,
                "color": "#4a6",
                "style": "p",
                "legend": "take profit",
                "width": 2,
            },
        ],
    }
