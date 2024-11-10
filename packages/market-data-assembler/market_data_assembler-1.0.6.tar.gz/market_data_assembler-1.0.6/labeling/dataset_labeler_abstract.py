from abc import ABC, abstractmethod
from typing import Dict, List

from assembling.aggregation_config import AggregationConfigInstance


class BaseDatasetLabeler(ABC):
    def __init__(self, training_window: float):
        self.training_window = training_window

    def apply(self, aggregations: List[AggregationConfigInstance]) -> Dict:
        labels = self.process_window(aggregations)
        return {'labels': labels}

    @abstractmethod
    def process_window(self, aggregations: List[AggregationConfigInstance]) -> Dict:
        pass

    def get_name(self):
        pass
