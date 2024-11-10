import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List

from aggregator.missing_candles_enricher import MissingCandlesEnricher
from assembling.aggregation_config import AggregationConfig
from assembling.dataset_assembler import DatasetAssembler
from assembling.dataset_cache import DatasetCache
from common.common import random_string, load_compressed_json, generate_date_range
from labeling.dataset_labeler_abstract import BaseDatasetLabeler


class HistoricalAssemblerManager:
    """Assembles a dataset from cryptocurrency series data."""

    dataset_out_root_folder = './out/datasets'

    def __init__(
            self,
            instruments: List[str],
            day_from: datetime,
            day_to: datetime,
            dataset_labeler: BaseDatasetLabeler,
            aggregations_configs: List[AggregationConfig],
            raw_series_folder: str,
            max_workers: int
    ):

        self.instruments = instruments
        self.aggregations_configs = aggregations_configs
        self.selected_days = generate_date_range(day_from, day_to)
        self.dataset_labeler: BaseDatasetLabeler = dataset_labeler
        self.raw_series_folder = raw_series_folder
        self.max_workers = max_workers
        self.dataset_unique_name = random_string()
        self.cache = DatasetCache(
            day_from,
            day_to,
            self.dataset_out_root_folder,
            self.instruments,
            self.aggregations_configs,
            self.dataset_labeler,
            self.dataset_unique_name
        )
        self.assembler: DatasetAssembler
        self.missing_candles_enricher: MissingCandlesEnricher

    def generate_dataset(self):
        datasets_path = self.cache.get_cached()
        if datasets_path:
            return datasets_path

        for instrument in self.instruments:
            self._process_instrument(instrument)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for instrument in self.instruments:
                futures.append(executor.submit(self._process_instrument, instrument))

            for future in as_completed(futures):
                future.result()

        datasets_path = self.cache.save_config()
        return datasets_path

    def _process_instrument(self, instrument):
        self._reset_state(instrument)
        for file_path in self._filter_and_sort_files(instrument):
            print(f"process-{os.getpid()}, time: {datetime.now()}, assembling file : {file_path}")
            series = load_compressed_json(file_path)
            for raw_candle in series:
                self._process_raw_candle(raw_candle, instrument)

    def _process_raw_candle(self, raw_candle, instrument):
        enriched_candles = self.missing_candles_enricher.generate(raw_candle)
        for candle in enriched_candles:
            self._process_aggregations(candle, instrument)

    def _reset_state(self, instrument):
        self.last_candle_time = 0
        self.assembler = DatasetAssembler(instrument=instrument, aggregations_configs=self.aggregations_configs)
        self.missing_candles_enricher = MissingCandlesEnricher(window=self.assembler.get_main_aggregation_window())

    def _process_aggregations(self, candle, instrument):
        self.assembler.update_aggregations(candle, instrument)

        if self.assembler.is_ready():
            labels = self.dataset_labeler.apply(self.assembler.get_aggregations())
            dataset = self.assembler.to_dataset()
            dataset.update(labels)
            self.cache.save_dataset(dataset, instrument)

    def _filter_and_sort_files(self, instrument):
        all_files = os.listdir(self.raw_series_folder)
        selected_days_naive = [day.replace(tzinfo=None) for day in self.selected_days]


        instrument_files = []
        for f in all_files:
            if f.startswith(instrument):
                date_str = f.split('_')[1].split('.')[0]
                file_date = datetime.strptime(date_str, '%Y-%m-%d')
                if file_date in selected_days_naive:
                    instrument_files.append((file_date, f))

        instrument_files.sort(key=lambda x: x[0])
        return [os.path.join(self.raw_series_folder, f[1]) for f in instrument_files]
