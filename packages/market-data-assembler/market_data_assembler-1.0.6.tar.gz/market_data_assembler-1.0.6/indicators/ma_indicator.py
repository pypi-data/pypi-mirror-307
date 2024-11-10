from indicators.indicator_abstract import BaseIndicator


class MovingAverageIndicator(BaseIndicator):

    def calculate_value(self) -> float:
        close_prices = [candle['c'] for candle in self.candles]
        return sum(close_prices) / len(close_prices)
