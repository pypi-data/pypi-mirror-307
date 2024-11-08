"""Functions to handle data uploads using Pandas."""

import pandas as pd
import pyarrow as pa

from timeseer_client.internal import MissingTimezoneException


def to_pyarrow_table(data: pd.DataFrame) -> pa.Table:
    """Converts a pandas dataframe to pyarrow."""
    data["ts"] = _ensure_utc_timezone(data["ts"])
    return pa.Table.from_pandas(data, preserve_index=False)


def _ensure_utc_timezone(ts: pd.Series):
    if ts.dt.tz is None:
        raise MissingTimezoneException()
    return ts.dt.tz_convert("UTC")
