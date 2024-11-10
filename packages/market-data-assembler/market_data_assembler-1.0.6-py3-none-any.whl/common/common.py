import os
import random
import shutil
import string
from datetime import timedelta, datetime
from typing import List

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def generate_date_range(day_from: datetime, day_to: datetime) -> List[datetime]:
    return [day_from + timedelta(days=i) for i in range((day_to - day_from).days + 1)]


def prepare_directory(folder) -> None:
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)


def random_string(length=10):
    return ''.join(random.choices(string.ascii_uppercase, k=length))


def save_compressed_json(data, file_path: str):
    df = pd.json_normalize(data)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, file_path, compression='ZSTD')


def load_compressed_json(file_path: str):
    table = pq.read_table(file_path)
    df = table.to_pandas()
    return df.to_dict(orient='records')
