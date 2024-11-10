from typing import List

from assembling.aggregation_config import AggregationConfig, AggregationConfigInstance


class DatasetAssembler:

    def __init__(self, instrument: str, aggregations_configs: List[AggregationConfig]):
        self.instrument = instrument
        self.aggregations_configs = aggregations_configs
        self.aggregations = AggregationConfigInstance.from_config_list(aggregations_configs)
        self.main_aggregation = AggregationConfigInstance.get_main_aggregation(self.aggregations)

    def get_main_aggregation_window(self):
        return self.main_aggregation.get_window_sec()

    def get_aggregations(self):
        return self.aggregations

    def update_aggregations(self, candle, instrument):
        for aggregator in self.aggregations:
            aggregator.ohlc.aggregate(candle, instrument)
            aggregated_candle = aggregator.ohlc.get_last_aggregated()
            for indicator in aggregator.indicators:
                indicator.apply(aggregated_candle)

    def is_ready(self):
        all_components_ready = all(
            aggregator.ohlc.is_ready() and all(indicator.is_ready() for indicator in aggregator.indicators)
            for aggregator in self.aggregations
        )
        return self.main_aggregation.ohlc.is_fully_aggregated() and all_components_ready

    def to_dataset(self):
        date_range = self.main_aggregation.get_time_period()
        aggregations = []

        for aggregator in self.aggregations:
            series = self._to_ohlc_dataset_map(aggregator.ohlc.get_history())

            indicators = [
                {
                    "indicator_class": indicator.__class__.__name__,
                    "window_length": indicator.window_length,
                    "values": indicator.get_history()
                }
                for indicator in aggregator.indicators
            ]

            aggregations.append({
                'ohlc': {
                    'window_sec': aggregator.ohlc.window_sec,
                    'history_size': aggregator.ohlc.history_size,
                    'series': series
                },
                'indicators': indicators
            })

        dataset = {
            'instrument': self.instrument,
            'from': date_range['from'],
            'to': date_range['to'],
            'aggregations': aggregations
        }

        return dataset

    @staticmethod
    def _to_ohlc_dataset_map(candles: List):
        series = {}
        for candle in candles:
            for c_key, c_value in candle.items():
                if c_key in ['o', 'c', 'h', 'l', 'v']:
                    series.setdefault(c_key, []).append(c_value)
        return series

    def get_info(self):
        info = {'instrument': self.instrument}
        info.update({'aggregations': {[aggregator.get_info() for aggregator in self.aggregations]}})

        return info
