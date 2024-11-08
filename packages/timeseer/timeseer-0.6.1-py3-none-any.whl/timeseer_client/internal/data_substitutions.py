"""Functions to handle data substitutions data."""

import pyarrow as pa

from timeseer_client.internal import DataSubstitutionData


def apply_data_substitution(
    original_data: pa.Table,
    data_substitution_data: DataSubstitutionData,
) -> pa.Table:
    """Apply a data substitution and return the resulting table."""
    has_quality = False
    substitution_data = data_substitution_data.data
    if "quality" in original_data.column_names:
        has_quality = True
        if has_quality and "quality" not in substitution_data.column_names:
            quality = pa.array([1] * len(substitution_data))
            substitution_data = substitution_data.append_column("quality", quality)
        if not has_quality and "quality" in substitution_data.column_names:
            substitution_data = substitution_data.drop_columns("quality")

    data = original_data.cast(substitution_data.schema)
    data_before = data.filter(
        pa.compute.less(data["ts"], pa.scalar(data_substitution_data.start_date))
    )
    data_after = data.filter(
        pa.compute.greater(data["ts"], pa.scalar(data_substitution_data.end_date))
    )

    return pa.concat_tables([data_before, substitution_data, data_after])


def mask_event_frames(data: pa.Table, event_frames: pa.Table) -> pa.Array:
    """Generate a boolean mask that is True for each data point in data were an event frame is active."""
    mask = pa.array([False] * len(data))

    for i in range(0, len(event_frames)):
        start_date = event_frames["start_date"][i]
        end_date = event_frames["end_date"][i]

        start_mask = pa.compute.greater_equal(data["ts"], start_date)
        end_mask = pa.compute.less(data["ts"], end_date)

        frame_mask = pa.compute.and_(start_mask, end_mask)
        mask = pa.compute.or_(mask, frame_mask)

    return mask
