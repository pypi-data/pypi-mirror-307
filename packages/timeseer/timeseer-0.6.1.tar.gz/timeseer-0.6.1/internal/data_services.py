"""Python client for Timeseer Data Services."""

import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import pyarrow as pa
from kukur import Metadata, SeriesSelector

from timeseer_client.internal import (
    DataServiceSelector,
    DataSubstitution,
    DataSubstitutionCursor,
    DataSubstitutionData,
    DataSubstitutionResponse,
    EventFrame,
    MissingSeriesSetException,
    ServerReturnedException,
    Statistic,
    TimeoutException,
    TimeseerClient,
    TimeseerClientException,
    parse_json_exception_message,
    parse_json_response,
)


class DataServiceEvaluationFailedException(TimeseerClientException):
    """Thrown when a data service evaluation fails."""

    def __init__(self, name: str, view_name: str):
        super().__init__(f'evaluation for data service "{name}"/"{view_name}" failed')


class DataServiceEvaluationsFailedException(TimeseerClientException):
    """Thrown when a data service evaluation fails."""

    def __init__(self, name: str):
        super().__init__(f'evaluations for data service "{name}" failed')


@dataclass()
class DataSubstitutionQuery:
    """Query options for fetching data substitutions."""

    data_service_selector: DataServiceSelector
    series_selector: Optional[SeriesSelector] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    last_modified_date: Optional[datetime] = None
    cursor: Optional[DataSubstitutionCursor] = None
    is_manual: Optional[bool] = None

    def to_data(self) -> dict[str, Any]:
        """Return a JSON object."""
        query_data: Dict[str, Any] = {
            "dataServiceName": self.data_service_selector.name
        }
        if self.data_service_selector.series_set_name is not None:
            query_data["dataServiceViewName"] = (
                self.data_service_selector.series_set_name
            )
        if self.series_selector is not None:
            query_data["selector"] = self.series_selector.to_data()
        if self.start_date is not None:
            query_data["startDate"] = self.start_date.isoformat()
        if self.end_date is not None:
            query_data["endDate"] = self.end_date.isoformat()
        if self.last_modified_date is not None:
            query_data["lastModifiedDate"] = self.last_modified_date.isoformat()
        if self.cursor is not None:
            query_data["cursor"] = self.cursor.to_data()
        if self.is_manual is not None:
            query_data["isManual"] = self.is_manual
        return query_data


class DataServices:
    """Data Services provide access to analysis results, time series data and statistics.

    Args:
        client: the Timeseer Client
    """

    __client: TimeseerClient

    def __init__(self, client: TimeseerClient):
        self.__client = client

    def list(self) -> List[str]:
        """Return a list containing all the Data Service names."""
        response = self.__client.request("GET", "data-services/")
        return [data_service["name"] for data_service in parse_json_response(response)]

    def get(self, data_service_name: str) -> List[DataServiceSelector]:
        """Return a list containing a selector for each series set in a data service."""
        response = self.__client.request(
            "GET",
            "data-services/views",
            query={"dataServiceName": data_service_name},
        )
        selector_data = parse_json_response(response)
        return [DataServiceSelector.from_data(data) for data in selector_data]

    def wait_for_all_evaluations(
        self, data_service_name: str, *, timeout_seconds: float = 60.0
    ) -> None:
        """Wait until all the evaluations of a Data Service are complete.

        Args:
            data_service_name: The name of the Data Service to wait for.
            timeout_seconds: The number of seconds to wait until the evaluation is complete. (optional, keyword only)

        Raises:
            DataServiceEvaluationsFailedException when a failure is reported.
        """
        query = {"dataServiceName": data_service_name}
        while timeout_seconds > 0:
            response = self.__client.request("GET", "data-services/state", query=query)
            job_states = parse_json_response(response)
            if all(
                job_state["completed"] == job_state["total"] for job_state in job_states
            ):
                if any(job_state["failed"] > 0 for job_state in job_states):
                    raise DataServiceEvaluationsFailedException(data_service_name)
                return
            time.sleep(0.2)
            timeout_seconds = timeout_seconds - 0.2

        raise TimeoutException()

    def wait_for_evaluation(
        self,
        data_service_selector: DataServiceSelector,
        *,
        timeout_seconds: int = 60,
    ) -> None:
        """Wait until the evaluation of a Data Service is complete.

        Args:
            data_service_selector: The series set in a Data Service to wait for.
            timeout_seconds: The number of seconds to wait until the evaluation is complete. (optional, keyword only)

        Raises:
            DataServiceEvaluationFailedException when a failure is reported.
        """
        if data_service_selector.series_set_name is None:
            raise MissingSeriesSetException()
        query = {
            "dataServiceName": data_service_selector.name,
            "dataServiceViewName": data_service_selector.series_set_name,
        }
        while timeout_seconds > 0:
            response = self.__client.request(
                "GET", "data-services/view/state", query=query
            )
            job_state = parse_json_response(response)
            if job_state["completed"] == job_state["total"]:
                if job_state["failed"] > 0:
                    raise DataServiceEvaluationFailedException(
                        data_service_selector.name,
                        data_service_selector.series_set_name,
                    )
                return
            time.sleep(1)
            timeout_seconds = timeout_seconds - 1

        raise TimeoutException()

    def get_data(
        self,
        data_service_selector: DataServiceSelector,
        series_selector: SeriesSelector,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> pa.Table:
        """Get data from a given Data Service.

        Falls back to the data source when no data is present.

        Args:
            data_service_selector: The series set in the Data Service to look for data in.
            series_selector: Return data for the time series selected by this selector.
            start_date: the start date of the data
                Defaults to start date of the data service.
            end_date: the end date of the data
                Defaults to end date of the data service.

        Returns::
            A pyarrow Table with three columns: 'ts', 'value' and 'quality'.
        """
        if data_service_selector.series_set_name is None:
            raise MissingSeriesSetException()
        body = {
            "dataServiceName": data_service_selector.name,
            "dataServiceViewName": data_service_selector.series_set_name,
            "selector": series_selector.to_data(),
            "startDate": start_date.isoformat() if start_date is not None else None,
            "endDate": end_date.isoformat() if end_date is not None else None,
        }

        response = self.__client.request(
            "POST",
            "data-services/view/get-data",
            body=body,
            headers={
                "Accept": "application/vnd.apache.arrow.stream",
            },
        )
        if response.status not in [200, 201]:
            raise ServerReturnedException(parse_json_exception_message(response))
        buffer = response.read()
        reader = pa.ipc.RecordBatchStreamReader(buffer)
        return reader.read_all()

    def list_data_substitutions(
        self, query: DataSubstitutionQuery
    ) -> DataSubstitutionResponse:
        """List data substitutions in a data service.

        Args:
            query: The query to filter the data substitutions.

        Returns::
            A list of `DataSubstitution`s
        """
        body = query.to_data()
        response = self.__client.request(
            "POST", "data-services/data-substitutions", body=body
        )
        response_data = parse_json_response(response)
        return DataSubstitutionResponse(
            (
                DataSubstitutionCursor.from_data(response_data["cursor"])
                if response_data["cursor"] is not None
                else None
            ),
            [
                DataSubstitution.from_data(substitution_data)
                for substitution_data in response_data["substitutions"]
            ],
        )

    def get_substitution_data(
        self,
        data_service_selector: DataServiceSelector,
        data_substitution: DataSubstitution,
    ) -> DataSubstitutionData:
        """Get the stored data for a given data substitution.

        Args:
            data_service_selector: The series set in the Data Service to look for data in.
            data_substitution: The data substitution to query the data for.

        Returns::
            A pyarrow Table with three columns: 'ts', 'value' and 'quality'.
        """
        if data_service_selector.series_set_name is None:
            raise MissingSeriesSetException()
        query = {
            "dataServiceName": data_service_selector.name,
            "dataServiceViewName": data_service_selector.series_set_name,
            "dataSubstitutionId": str(data_substitution.db_id),
        }

        response = self.__client.request(
            "GET",
            "data-services/view/get-substitution-data",
            query=query,
            headers={
                "Accept": "application/vnd.apache.arrow.stream",
            },
        )
        if response.status not in [200, 201]:
            raise ServerReturnedException(parse_json_exception_message(response))
        buffer = response.read()
        reader = pa.ipc.RecordBatchStreamReader(buffer)
        return DataSubstitutionData(
            data_substitution.start_date, data_substitution.end_date, reader.read_all()
        )

    def get_kpi_scores(
        self, data_service_selector: DataServiceSelector
    ) -> Dict[str, int]:
        """Get the kpi scores of a Data Service.

        Args:
            data_service_selector: The series set in the Data Service to return scores for.

        Returns::
            The score per KPI as a percentage.
        """
        if data_service_selector.series_set_name is None:
            raise MissingSeriesSetException()
        query = {
            "dataServiceName": data_service_selector.name,
            "dataServiceViewName": data_service_selector.series_set_name,
        }
        response = self.__client.request(
            "GET", "data-services/view/kpi-scores", query=query
        )
        return parse_json_response(response)

    def convert_to_event_frame(self, table: pa.Table) -> List[EventFrame]:
        """Convert a PyArrow table to an EventFrame object."""
        return [EventFrame.from_row(data) for data in table.to_pylist()]

    def get_event_frames(  # noqa: PLR0913
        self,
        data_service_selector: DataServiceSelector,
        series_selector: Optional[SeriesSelector] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        frame_type: Optional[Union[str, List[str]]] = None,
        last_modified_date: Optional[datetime] = None,
    ) -> pa.Table:
        """Get all event frames matching the given criteria.

        Args:
            data_service_selector: The series set in the Data Service to return event frames for.
            series_selector: the time series to which the event frames are linked.
            start_date: the start date of the range to find overlapping event frames in.
                Defaults to start date of the data service.
            end_date: the end date of the range to find overlapping event frames in.
                Defaults to end date of the data service.
            frame_type: the type or types of event frames to search for. Finds all types when empty.
            last_modified_date: only include event frames modified on or later than this timestamp.

        Returns::
            A pyarrow Table with 9 columns.
            The first column ('start_date') contains the start date.
            The second column ('end_date') contains the end date.
            The third column ('type') contains the type of the returned event frame as a string.
            The fourth column ('explanation') can contain the explanation for an event frame as a string.
            The fifth column ('status') can contain the status of an event frame as a string.
            Columns 6 contains possible multiple references for the event frame.
            the seventh column contains the properties of the event frame.
            The eighth column contains the uuid of the event frame.
            The ninth column contains the last modified timestamp of the event frame.
        """
        if data_service_selector.series_set_name is None:
            raise MissingSeriesSetException()
        body: Dict[str, Any] = {
            "dataServiceName": data_service_selector.name,
            "dataServiceViewName": data_service_selector.series_set_name,
            "selector": (
                series_selector.to_data() if series_selector is not None else None
            ),
            "startDate": start_date.isoformat() if start_date is not None else None,
            "endDate": end_date.isoformat() if end_date is not None else None,
            "lastModifiedDate": (
                last_modified_date.isoformat()
                if last_modified_date is not None
                else None
            ),
        }

        if frame_type is not None:
            body["type"] = frame_type

        response = self.__client.request(
            "POST",
            "data-services/view/event-frames",
            body=body,
            headers={
                "Accept": "application/vnd.apache.arrow.stream",
            },
        )
        if response.status not in [200, 201]:
            raise ServerReturnedException(parse_json_exception_message(response))
        buffer = response.read()
        reader = pa.ipc.RecordBatchStreamReader(buffer)
        return reader.read_all()

    def update_event_frame(self, event_frame: EventFrame):
        """Update the properties on an event frame.

        Args:
            event_frame: The event frame to be updated.
        """
        body = {
            "eventFrame": event_frame.to_data(),
        }
        self.__client.request(
            "POST", "data-services/view/event-frames/update", body=body
        )

    def delete_multivariate_event_frame(  # noqa: PLR0913
        self,
        data_service_selector: DataServiceSelector,
        start_date: datetime,
        end_date: datetime,
        frame_type: str,
    ):
        """Create a multivariate event frame.

        Args:
            data_service_selector: The series set in the data_service to create an event frame for.
            start_date: the start date of the range to find overlapping event frames in.
                Defaults to start date of the data service.
            end_date: the end date of the range to find overlapping event frames in.
                Defaults to end date of the data service.
            frame_type: the type or types of event frames to search for. Finds all types when empty.
        """
        if data_service_selector.series_set_name is None:
            raise MissingSeriesSetException()
        event_frame = {
            "type": frame_type,
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat(),
        }

        body = {
            "dataServiceName": data_service_selector.name,
            "dataServiceViewName": data_service_selector.series_set_name,
            "eventFrames": [event_frame],
        }
        self.__client.request("DELETE", "data-services/view/event-frames", body=body)

    def create_multivariate_event_frame(  # noqa: PLR0913
        self,
        data_service_selector: DataServiceSelector,
        start_date: datetime,
        end_date: datetime,
        frame_type: str,
    ):
        """Create a multivariate event frame.

        Args:
            data_service_selector: The series set in the data_service to create an event frame for.
            start_date: the start date of the range to find overlapping event frames in.
                Defaults to start date of the data service.
            end_date: the end date of the range to find overlapping event frames in.
                Defaults to end date of the data service.
            frame_type: the type or types of event frames to search for. Finds all types when empty.
        """
        if data_service_selector.series_set_name is None:
            raise MissingSeriesSetException()
        event_frame = {
            "type": frame_type,
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat(),
        }

        body = {
            "dataServiceName": data_service_selector.name,
            "dataServiceViewName": data_service_selector.series_set_name,
            "eventFrames": [event_frame],
        }
        self.__client.request(
            "POST", "data-services/view/event-frames/create", body=body
        )

    def delete_event_frame(  # noqa: PLR0913
        self,
        data_service_selector: DataServiceSelector,
        series_selector: SeriesSelector,
        start_date: datetime,
        end_date: datetime,
        frame_type: str,
    ):
        """Delete a univariate event frame.

        Args:
            data_service_selector: the series set in the data_service to create an event frame for.
            series_selector: the time series to which the event frame is linked.
            start_date: the start date of the event frame.
            end_date: the end date of the event frame.
            frame_type: the type of the event frame.
        """
        if data_service_selector.series_set_name is None:
            raise MissingSeriesSetException()
        event_frame = {
            "type": frame_type,
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat(),
        }

        body = {
            "dataServiceName": data_service_selector.name,
            "dataServiceViewName": data_service_selector.series_set_name,
            "selector": series_selector.to_data(),
            "eventFrames": [event_frame],
        }
        self.__client.request("DELETE", "data-services/view/event-frames", body=body)

    def create_event_frame(  # noqa: PLR0913
        self,
        data_service_selector: DataServiceSelector,
        series_selector: SeriesSelector,
        start_date: datetime,
        end_date: datetime,
        frame_type: str,
    ):
        """Create a univariate event frame.

        Args:
            data_service_selector: the series set in the data_service to create an event frame for.
            series_selector: the time series to which the event frame is linked.
            start_date: the start date of the event frame.
            end_date: the end date of the event frame.
            frame_type: the type of the event frame.
        """
        if data_service_selector.series_set_name is None:
            raise MissingSeriesSetException()
        event_frame = {
            "type": frame_type,
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat(),
        }

        body = {
            "dataServiceName": data_service_selector.name,
            "dataServiceViewName": data_service_selector.series_set_name,
            "selector": series_selector.to_data(),
            "eventFrames": [event_frame],
        }
        self.__client.request(
            "POST", "data-services/view/event-frames/create", body=body
        )

    def list_series(
        self, data_service_selector: DataServiceSelector
    ) -> List[SeriesSelector]:
        """Return all series in a Data Service Series Set.

        Args:
            data_service_selector: The series set in the Data Service to list series for.

        Returns::
            A list of `SeriesSelector`s.
        """
        if data_service_selector.series_set_name is None:
            raise MissingSeriesSetException()
        query = {
            "dataServiceName": data_service_selector.name,
            "dataServiceViewName": data_service_selector.series_set_name,
        }
        response = self.__client.request(
            "GET", "data-services/view/series", query=query
        )
        return [
            SeriesSelector.from_data(data) for data in parse_json_response(response)
        ]

    def get_statistics(
        self,
        data_service_selector: DataServiceSelector,
        series_selector: Optional[SeriesSelector] = None,
    ) -> List[Statistic]:
        """Return statistics stored in a Data Service.

        Returns multivariate and calculated statistics for a series set if no SeriesSelector is provided.

        Args:
            data_service_selector: The series set in the Data Service to return statistics for.
            series_selector: The time series to return statistics for. (optional, keyword-only)

        Returns::
            A list of `Statistic`s.
        """
        if data_service_selector.series_set_name is None:
            raise MissingSeriesSetException()
        body: Dict[str, Any] = {
            "dataServiceName": data_service_selector.name,
            "dataServiceViewName": data_service_selector.series_set_name,
        }

        if series_selector is not None:
            body["selector"] = series_selector.to_data()

        response = self.__client.request(
            "POST", "data-services/view/statistics", body=body
        )
        return [Statistic.from_data(data) for data in parse_json_response(response)]

    def get_calculated_metadata(
        self,
        data_service_selector: DataServiceSelector,
        selector: SeriesSelector,
    ) -> Metadata:
        """Return calculated metadata for a series in a Data Service.

        Args:
            data_service_selector: The series set in a Data Service where the calculated metadata is kept.
            selector: The time series to return calculated metadata for.

        Returns::
            A `Metadata` object with the calculated metadata that's available.
        """
        if data_service_selector.series_set_name is None:
            raise MissingSeriesSetException()
        body: Dict[str, Any] = {
            "dataServiceName": data_service_selector.name,
            "dataServiceViewName": data_service_selector.series_set_name,
            "selector": selector.to_data(),
        }
        response = self.__client.request(
            "POST", "data-services/view/calculated-metadata", body=body
        )
        return Metadata.from_data(
            parse_json_response(response),
            selector,
        )
