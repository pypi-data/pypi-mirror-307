"""Test data substitusions."""

from datetime import datetime

import pyarrow.compute as pc
from pyarrow import Table

from timeseer_client import apply_data_substitution
from timeseer_client.internal import DataSubstitutionData


def test_substitute_edges() -> None:
    original_data = Table.from_pydict(
        {
            "ts": [
                datetime.fromisoformat("2024-01-01T00:00:00Z"),
                datetime.fromisoformat("2024-01-02T00:00:00Z"),
                datetime.fromisoformat("2024-01-03T00:00:00Z"),
                datetime.fromisoformat("2024-01-04T00:00:00Z"),
                datetime.fromisoformat("2024-01-05T00:00:00Z"),
            ],
            "value": [
                1.0,
                float("NaN"),
                float("NaN"),
                float("NaN"),
                5.0,
            ],
        }
    )
    substitution = DataSubstitutionData(
        datetime.fromisoformat("2024-01-02T00:00:00Z"),
        datetime.fromisoformat("2024-01-04T00:00:00Z"),
        Table.from_pydict(
            {
                "ts": [
                    datetime.fromisoformat("2024-01-02T00:00:00Z"),
                    datetime.fromisoformat("2024-01-03T00:00:00Z"),
                    datetime.fromisoformat("2024-01-04T00:00:00Z"),
                ],
                "value": [2.0, 3.0, 4.0],
            }
        ),
    )

    result = apply_data_substitution(original_data, substitution)
    assert pc.all(pc.invert(pc.is_nan(result["value"]))).as_py()
    assert len(result) == 5
    assert pc.sum(result["value"]).as_py() == 15
