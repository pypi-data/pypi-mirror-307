"""Python client for Timeseer Data Sets."""

from typing import Any, List, Tuple

import pyarrow as pa
from kukur import Metadata

from timeseer_client.internal import (
    MissingTimezoneException,
    TimeseerClient,
    UnsupportedDataFormatException,
    parse_json_response,
)

HAS_PANDAS = True
try:
    import pandas as pd

    from timeseer_client.internal import data_uploader_pandas

except Exception:
    HAS_PANDAS = False


class DataSets:
    """Data Sets are fixed collections of time series and their data in a specific time range.

    Args:
        client: the Timeseer Client
    """

    __client: TimeseerClient

    def __init__(self, client: TimeseerClient):
        self.__client = client

    def list(self) -> List[str]:
        """Return a list containing all the data set names."""
        response = self.__client.request("GET", "data-sets/")
        return [data_service["name"] for data_service in parse_json_response(response)]

    def remove_data(self, name: str):
        """Removes all data in a data set.

        Args:
            name: The name of the data set.
        """
        body = {"name": name}
        self.__client.request("POST", "data-sets/remove-data", body=body)

    def upload_data(
        self,
        many_series: List[Tuple[Metadata, Any]],
    ):
        """Upload time series data to a Data Set.

        The 'source' field in the SeriesSelector in Metadata determines the name of the data set.

        Data is provided as a pyarrow.Table or pandas DataFrame of two or three columns:
            The first column with name 'ts' contains Arrow timestamps.
            The second column with name 'value' contains the values as a number or string.
            The optional third column with name 'quality' contains a quality flag (0 is BAD, 1 is GOOD)

        Arguments:
            many_series: a list of tuple of metadata and data.
        """
        for metadata, table in many_series:
            if isinstance(table, pa.Table):
                data = _ensure_utc_timezone(table)
            elif HAS_PANDAS and isinstance(table, pd.DataFrame):
                data = data_uploader_pandas.to_pyarrow_table(table)
            else:
                raise UnsupportedDataFormatException()
            metadata_json = metadata.to_data()
            self.__client.do_put(metadata_json, data)


def _ensure_utc_timezone(table: pa.Table) -> pa.Table:
    if table.schema.field("ts").type.tz is None:
        raise MissingTimezoneException()

    return table.set_column(
        table.column_names.index("ts"),
        "ts",
        pa.compute.cast(table["ts"], pa.timestamp("us", "UTC")),
    )
