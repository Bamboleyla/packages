from typing import TypedDict, List, Literal
from myLib.strategies.withDoubleTrend.types import DoubleTrendSignals


class PlotConfig(TypedDict):
    column: str
    color: str
    width: int


class ActionConfig(TypedDict):
    column: str
    color: str
    style: str
    width: int


class SignalConfig(TypedDict):
    name: DoubleTrendSignals
    price_col: str
    offset: int
    color: str
    style: Literal["^", "o", "p"]
    legend: str
    width: int


class PlotDataTypedDict(TypedDict):
    legend: str
    required_columns: List[str]
    plots: List[PlotConfig]
    actions: List[ActionConfig]
    signals: List[SignalConfig]
