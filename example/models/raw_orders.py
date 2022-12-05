import random
from datetime import datetime, timedelta

import pandas as pd

from example.helper import iter_dates
from sqlmesh import EngineAdapter, model
from sqlmesh.utils.date import to_ds

CUSTOMERS = list(range(0, 100))
WAITERS = list(range(0, 10))


@model(
    """
    MODEL(
        name raw.orders,
        kind incremental,
        time_column ds,
        start '2022-01-01',
        cron '@daily',
        batch_size 30,
        columns (
            id int,
            customer_id int,
            waiter_id int,
            start_ts int,
            end_ts int,
            ds text,
        ),
    )
    """
)
def execute(
    engine: EngineAdapter,
    start: datetime,
    end: datetime,
    latest: datetime,
    **kwargs,
) -> pd.DataFrame:
    dfs = []
    for dt in iter_dates(start, end):
        num_orders = random.randint(10, 30)

        start_ts = [
            int((dt + timedelta(seconds=random.randint(0, 80000))).timestamp())
            for _ in range(num_orders)
        ]

        end_ts = [int(s + random.randint(0, 60 * 60)) for s in start_ts]

        dfs.append(
            pd.DataFrame(
                {
                    "customer_id": random.choices(CUSTOMERS, k=num_orders),
                    "waiter_id": random.choices(WAITERS, k=num_orders),
                    "start_ts": start_ts,
                    "end_ts": end_ts,
                    "ds": to_ds(dt),
                }
            )
            .reset_index()
            .rename(columns={"index": "id"})
        )

    return pd.concat(dfs)
