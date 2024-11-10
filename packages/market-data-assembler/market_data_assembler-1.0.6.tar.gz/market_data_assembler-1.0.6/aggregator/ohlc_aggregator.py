from datetime import datetime, timedelta, timezone
import numpy as np

class OHLCAggregator:
    def __init__(self, window_sec, history_size):
        self.start_time = None
        self.history_size = history_size
        self.window_sec = window_sec
        self.current_window_candles = []
        self.history = []

    @staticmethod
    def _parse_datetime(timestamp_ms):
        return datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)

    def _flatten(self, data):
        flat_list = []
        if isinstance(data, dict):
            flat_list.append(data)
        elif isinstance(data, (list, np.ndarray)):
            for item in data:
                flat_list.extend(self._flatten(item))
        return flat_list

    def _aggregate_candles(self, end_time):
        open_price = self.current_window_candles[0]['o']
        close_price = self.current_window_candles[-1]['c']
        high_price = max(candle['h'] for candle in self.current_window_candles)
        low_price = min(candle['l'] for candle in self.current_window_candles)
        volume = sum(candle['v'] for candle in self.current_window_candles)
        total_trades = sum(candle['n'] for candle in self.current_window_candles)

        aggregated_trades = []
        for candle in self.current_window_candles:
            trades = candle.get('trades')
            if isinstance(trades, (list, np.ndarray)):
                for trade in self._flatten(trades):
                    if isinstance(trade, dict) and 't' in trade:
                        aggregated_trades.append(trade)

        if aggregated_trades:
            aggregated_trades.sort(key=lambda trade: trade['t'])

        aggregated_books = []
        for candle in self.current_window_candles:
            book_depth = candle.get('book_depth')
            if isinstance(book_depth, (list, np.ndarray)):
                for book in self._flatten(book_depth):
                    if isinstance(book, dict) and 't' in book:
                        aggregated_books.append(book)

        if aggregated_books:
            aggregated_books.sort(key=lambda book: book['t'])

        t = int(end_time.timestamp() * 1000)

        aggregated_candle = {
            "t": t,
            "o": open_price,
            "h": high_price,
            "l": low_price,
            "c": close_price,
            "v": volume,
            "n": total_trades,
            "trades": aggregated_trades,
            "book_depth": aggregated_books
        }

        return aggregated_candle

    def aggregate(self, new_candle, instrument):
        candle_time = self._parse_datetime(new_candle["t"])

        if self.start_time is None:
            self.start_time = candle_time - timedelta(seconds=candle_time.second % self.window_sec,
                                                      microseconds=candle_time.microsecond)

        window_end_time = self.start_time + timedelta(seconds=self.window_sec)
        window_end_time_x2_check = self.start_time + timedelta(seconds=self.window_sec * 2)

        if candle_time >= window_end_time:
            if candle_time >= window_end_time_x2_check or not self.current_window_candles:
                raise ValueError(f"Out of aggregation window range or nothing to aggregate. {instrument}, {new_candle['t']}")

            aggregated_candle = self._aggregate_candles(window_end_time)
            self.start_time = window_end_time
            self.current_window_candles = [new_candle]

        else:
            self.current_window_candles.append(new_candle)
            aggregated_candle = self._aggregate_candles(window_end_time)

        if self._need_replace_last_candle(aggregated_candle):
            if self.history:
                self.history.pop()
        self.history.append(aggregated_candle)

        if len(self.history) > self.history_size:
            self.history.pop(0)

    def _need_replace_last_candle(self, new_candle):
        return self.history and self.history[-1]["t"] == new_candle["t"]

    def is_ready(self):
        return len(self.history) == self.history_size

    def get_history(self):
        return self.history

    def is_fully_aggregated(self):
        return len(self.current_window_candles) == 1

    def get_last_aggregated(self):
        return self.history[-1]