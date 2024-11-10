import json
import os
from datetime import datetime

import mplfinance as mpf
import pandas as pd

json_path = 'ETHUSDT_1730424300000.json'
with open(json_path, 'r') as file:
    data = json.load(file)

output_dir = os.path.dirname(json_path)

base_timestamp_ms = data['from']
aggregations = data['aggregations']


def process_aggregation(aggregation, index):
    ohlc_data = aggregation['ohlc']
    window_sec = ohlc_data['window_sec']
    history_size = ohlc_data['history_size']
    series = ohlc_data['series']
    indicators = aggregation['indicators']

    timestamps = [
        datetime.utcfromtimestamp((base_timestamp_ms + i * window_sec * 1000) / 1000)
        for i in range(history_size)
    ]

    df = pd.DataFrame({
        'Open': series['o'],
        'High': series['h'],
        'Low': series['l'],
        'Close': series['c'],
        'Volume': series['v']
    }, index=timestamps)

    indicator_values = indicators[0]['values']
    df['Indicator'] = indicator_values

    addplots = [mpf.make_addplot(df['Indicator'], color='orange', width=0.5)]
    output_file = os.path.join(output_dir, f"{json_path}_ohlc_chart_{index}.png")
    mpf.plot(
        df,
        type='candle',
        style='charles',
        volume=True,
        addplot=addplots,
        title=f"OHLC Chart with Indicator (Window: {window_sec} sec)",
        ylabel='Price',
        ylabel_lower='Volume',
        datetime_format='%Y-%m-%d %H:%M',
        figsize=(12, 8),
        savefig=output_file
    )
    print(f"График сохранён: {output_file}")


for idx, aggregation in enumerate(aggregations):
    process_aggregation(aggregation, idx)
