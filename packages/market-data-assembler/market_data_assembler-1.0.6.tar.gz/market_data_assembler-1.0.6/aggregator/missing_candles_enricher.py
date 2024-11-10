import numpy as np

class MissingCandlesEnricher:
    def __init__(self, window: int):
        self.window = window
        self.last_candle = None

    def reset(self):
        self.last_candle = None

    def generate(self, new_candle):
        missing_candles = []

        if self.last_candle is None:
            return self._initialize_first_candle(new_candle, missing_candles)

        time_diff = self._calculate_time_difference(new_candle)

        if time_diff == self.window:
            self._add_new_candle(new_candle, missing_candles)
        elif time_diff > self.window:
            self._generate_missing_candles(new_candle, time_diff, missing_candles)
        else:
            self._update_last_candle(new_candle, missing_candles)

        return missing_candles

    def _initialize_first_candle(self, new_candle, missing_candles):
        self.last_candle = new_candle
        missing_candles.append(new_candle)
        return missing_candles

    def _calculate_time_difference(self, new_candle):
        last_time = self.last_candle['t']
        new_time = new_candle['t']
        return (new_time - last_time) // 1000

    def _add_new_candle(self, new_candle, missing_candles):
        self.last_candle = new_candle
        missing_candles.append(new_candle)

    def _generate_missing_candles(self, new_candle, time_diff, missing_candles):
        num_missing_candles = time_diff // self.window
        for i in range(1, num_missing_candles + 1):
            missing_time = self.last_candle['t'] + i * self.window * 1000
            if missing_time < new_candle['t']:
                missing_candle = self._create_missing_candle(missing_time)
                missing_candles.append(missing_candle)
                self.last_candle = missing_candle
            else:
                self._add_new_candle(new_candle, missing_candles)

    def _create_missing_candle(self, timestamp):
        return {
            't': timestamp,
            'o': self.last_candle['c'],
            'h': self.last_candle['c'],
            'l': self.last_candle['c'],
            'c': self.last_candle['c'],
            'v': 0.0,
            'n': 0,
            'trades': np.array([]),
            'book_depth': np.array([]),
        }

    def _update_last_candle(self, new_candle, missing_candles):
        self.last_candle = new_candle
        missing_candles.append(new_candle)
