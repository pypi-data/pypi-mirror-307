from typing import List, Type, TypedDict

from aggregator.ohlc_aggregator import OHLCAggregator
from indicators.indicator_abstract import BaseIndicator


class OHLCConfig(TypedDict):
    window_sec: int
    history_size: int


class IndicatorConfig(TypedDict):
    indicator_class: Type[BaseIndicator]
    window_length: int


class AggregationConfig(TypedDict):
    ohlc: OHLCConfig
    indicators: List[IndicatorConfig]


class AggregationConfigInstance:
    def __init__(self, config: AggregationConfig):
        self.ohlc = OHLCAggregator(
            window_sec=config["ohlc"]["window_sec"],
            history_size=config["ohlc"]["history_size"]
        )

        self.indicators = [
            indicator["indicator_class"](indicator["window_length"], config["ohlc"]["history_size"])
            for indicator in config["indicators"]
        ]

    def get_window_sec(self) -> int:
        return self.ohlc.window_sec

    def get_info(self) -> dict:
        info = {
            "window_sec": self.ohlc.window_sec,
            "history_size": self.ohlc.history_size,
            "indicators": []
        }

        for indicator in self.indicators:
            indicator_info = {
                "indicator_class": indicator.__class__.__name__,
                "window_length": indicator.window_length
            }
            info["indicators"].append(indicator_info)

        return info

    def get_time_period(self) -> dict:
        t_values = []
        for candle in self.ohlc.get_history():
            for c_key, c_value in candle.items():
                if c_key == 't':
                    t_values.append(c_value)

        return {
            'from': min(t_values),
            'to': max(t_values),
        }

    @staticmethod
    def from_config_list(configs: List[AggregationConfig]) -> List['AggregationConfigInstance']:
        return [AggregationConfigInstance(config) for config in configs]

    @staticmethod
    def get_main_aggregation(instances: List['AggregationConfigInstance']) -> 'AggregationConfigInstance':
        return min(instances, key=lambda instance: instance.ohlc.window_sec)
