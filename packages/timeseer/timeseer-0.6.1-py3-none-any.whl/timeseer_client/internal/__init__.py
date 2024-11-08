"""Implementation details for the Timeseer Client.

Only use classes and functions defined in timeseer_client.
"""

import json
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from http.client import HTTPResponse
from typing import Any, Dict, List, Optional, Protocol, Union

import pyarrow as pa
from kukur import SeriesSelector


class AugmentationStrategy(Enum):
    """AugmentationStrategy dictates what happens to filtered data points while augmenting based on event frames."""

    REMOVE = "remove values"
    HOLD_LAST = "hold last value"
    LINEAR_INTERPOLATION = "linear interpolation"
    KNN_IMPUTATION = "knn imputation"
    MEAN = "mean"


class TimeseerClientException(Exception):
    """Base class for Timeseer client exceptions.

    Use this to catch any exception that originates in the client.
    """


class UnauthorizedException(TimeseerClientException):
    """Raised when a request is not authorized to proceed with the given credentials."""


class TransportException(TimeseerClientException):
    """Raised when an unexpected error happened on the transport layer."""

    def __init__(self, status_code: int, message: str):
        super().__init__(f"HTTP status {status_code}: {message}")


class TooManyRedirectsException(TimeseerClientException):
    """Raised when a requests is in a redirect loop."""


class AugmentationException(TimeseerClientException):
    """Exception raised when augmentation strategy fails."""


class UnknownAugmentationStrategyException(TimeseerClientException):
    """Raised when the augmentation strategy is not known."""


class MissingModuleException(TimeseerClientException):
    """Raised when a required Python module is not available."""

    def __init__(self, module_name: str):
        TimeseerClientException.__init__(
            self,
            f'missing Python package: "{module_name}"',
        )


class ServerReturnedException(TimeseerClientException):
    """Raised when the server returns an error in the response body."""

    def __init__(self, error: str):
        TimeseerClientException.__init__(
            self,
            f'Exception returned by server: "{error}"',
        )


class MissingTimezoneException(TimeseerClientException):
    """Raised when a specified timeout is exceeded."""


class MissingSeriesSetException(TimeseerClientException):
    """Raised when the data service series set name is not provided."""


class UnsupportedDataFormatException(TimeseerClientException):
    """Raised when the data to upload is not in a supported format."""


class TimeoutException(TimeseerClientException):
    """Raised when a specified timeout is exceeded."""


class ProcessType(Enum):
    """ProcessType represents the process type of a time series."""

    CONTINUOUS = "CONTINUOUS"
    REGIME = "REGIME"
    BATCH = "BATCH"
    COUNTER = "COUNTER"


@dataclass
class Statistic:
    """Statistic represents a statistics that has been calculated.

    Statistics have a name and data type and contain a result that is specific per data type.
    """

    name: str
    data_type: str
    result: Any

    @classmethod
    def from_data(cls, data: dict[str, Any]):
        """Create a Statistic from a data dictionary."""
        name: str = data["name"]
        data_type: str = data["dataType"]
        if data_type == "datetime":
            result: Any = datetime.fromisoformat(data["result"])
        else:
            result = data["result"]
        return Statistic(name, data_type, result)


@dataclass
class Paging:
    """Paging information."""

    page: int
    page_size: int

    def to_data(self) -> Dict[str, Any]:
        """Convert to a dictionary suitable for JSON conversion."""
        return {
            "page": self.page,
            "pageSize": self.page_size,
        }


class EventFrameSeverity(Enum):
    """Severity of an event frame."""

    AT_RISK = "atRisk"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


@dataclass
class EventFrame:
    """EventFrame represents the event frames that were found."""

    start_date: datetime
    end_date: datetime
    type: str
    explanation: Optional[str]
    status: Optional[str]
    reference: Optional[list[SeriesSelector]]
    properties: Optional[dict[str, Union[str, float]]]
    uuid: str
    last_modified_date: Optional[datetime]
    severity: Optional[EventFrameSeverity] = None

    @classmethod
    def from_row(cls, data: dict[str, Any]):
        """Create an EventFrame from a pyarrow table row."""
        last_modified_date = None
        if data.get("last_modified_date") is not None:
            last_modified_date = data["last_modified_date"]
        reference = None
        if data.get("reference") is not None:
            if isinstance(data["reference"], dict):
                reference = [SeriesSelector.from_data(data["reference"])]
            else:
                reference = [
                    SeriesSelector.from_data(reference_data)
                    for reference_data in data["reference"]
                ]
        return EventFrame(
            data["start_date"],
            data["end_date"],
            data["type"],
            data.get("explanation"),
            data.get("status"),
            reference,
            data.get("properties"),
            data["uuid"],
            last_modified_date,
            None,
        )

    @classmethod
    def from_data(cls, data: dict[str, Any]):
        """Create an EventFrame from a dictionary."""
        last_modified_date = None
        if data.get("last_modified_date") is not None:
            last_modified_date = data["last_modified_date"]
        reference = None
        if data.get("reference") is not None:
            if isinstance(data["reference"], dict):
                reference = [SeriesSelector.from_data(data["reference"])]
            else:
                reference = [
                    SeriesSelector.from_data(reference_data)
                    for reference_data in data["reference"]
                ]
        severity = None
        if data.get("severity") is not None:
            severity = EventFrameSeverity(data["severity"])
        return EventFrame(
            data["startDate"],
            data["endDate"],
            data["type"],
            data.get("explanation"),
            data.get("status"),
            reference,
            data.get("properties"),
            data["uuid"],
            last_modified_date,
            severity,
        )

    def to_data(self) -> dict[str, Any]:
        """Convert to a dictionary suitable for JSON conversion."""
        end_date = None
        if self.end_date is not None:
            end_date = self.end_date.isoformat()

        data = {
            "startDate": self.start_date.isoformat(),
            "endDate": end_date,
            "type": self.type,
            "explanation": self.explanation,
            "status": self.status,
            "reference": (
                [reference.to_data() for reference in self.reference]
                if self.reference is not None
                else None
            ),
            "properties": json.dumps(self.properties),
            "uuid": self.uuid,
        }
        if self.last_modified_date is not None:
            data["lastModifiedDate"] = self.last_modified_date.isoformat()

        return data


@dataclass
class DataSubstitutionData:
    """Represents a stored data substitution."""

    start_date: datetime
    end_date: datetime
    data: pa.Table


class DataSubstitutionCursor:
    """Cursor into a stream of data substitutions of a data service."""

    def __init__(self, id: int):
        self.__id = id

    @classmethod
    def from_data(cls, data: dict) -> "DataSubstitutionCursor":
        """Create a new DataSubstitutionCursor from a data dictionary."""
        return cls(data["id"])

    def to_data(self) -> dict:
        """Convert to a data dictionary."""
        return {"id": self.__id}


class TimeseerClient(Protocol):
    """HTTP client to provide functionality to the python SDK."""

    def request(  # noqa PLR0913
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        body: Optional[Union[str, Dict[str, Any]]] = None,
        query: Optional[Dict[str, str]] = None,
    ) -> HTTPResponse:
        """Perform a request to the Timeseer server.

        Args:
            method: the HTTP method to use.
            url: the URL to request.
            headers: optional headers to send.
            body: optional body to send.

        Returns:
            The response from the server.
        """
        ...

    def do_put(self, data: Any, table: pa.Table) -> Any:
        """Do an Arrow Flight PUT request to upload an Arrow table.

        Args:
            data: The json-convertible data for the Flight descriptor.
            table: The pyarrow.Table to PUT.

        Returns:
            The json-converted result of the PUT operation.

        Raises:
            ServerReturnedException when the server returns an error in the response
            body instead of the result of the PUT operation.
        """
        ...


@dataclass
class DataServiceSelector:
    """Points to a series set inside a Data Service."""

    name: str
    series_set_name: Optional[str] = None

    @classmethod
    def from_data(cls, data: Dict[str, str]) -> "DataServiceSelector":
        """Create a DataServiceSelector from a JSON dictionary."""
        return cls(data["name"], data.get("view"))

    def to_data(self) -> Dict[str, str]:
        """Convert to a dictionary suitable for JSON conversion."""
        data = {"name": self.name}
        if self.series_set_name is not None:
            data["view"] = self.series_set_name
        return data


@dataclass
class DataSubstitution:
    """Represents a data substitution on series data."""

    db_id: int
    series: SeriesSelector
    data_service_selector: DataServiceSelector
    start_date: datetime
    end_date: datetime
    strategy: str
    value: Optional[float]
    limit: Optional[str]
    sample_rate: Optional[int]
    source_unit: Optional[str]
    target_unit: Optional[str]
    last_modified_date: datetime
    spread: bool

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "DataSubstitution":
        """Create a new instance from a dict."""
        return cls(
            data["id"],
            SeriesSelector.from_data(data["series"]),
            DataServiceSelector.from_data(data["dataServiceSelector"]),
            datetime.fromisoformat(data["startDate"]),
            datetime.fromisoformat(data["endDate"]),
            data["strategy"],
            data.get("value"),
            data.get("limit"),
            data.get("sampleRate"),
            data.get("sourceUnit"),
            data.get("targetUnit"),
            datetime.fromisoformat(data["lastModifiedDate"]),
            data.get("spread", False),
        )


@dataclass
class DataSubstitutionResponse:
    """Response of a list query for data substitutions.

    Contains a cursor that can be used to query only substitutions that were not seen before.
    """

    cursor: Optional[DataSubstitutionCursor]
    substitutions: List[DataSubstitution]


def parse_json_response(response: HTTPResponse) -> Any:
    """Parse a JSON response from the server."""
    data = response.read()
    return json.loads(data)["body"]


def parse_json_exception_message(response: HTTPResponse) -> str:
    """Parse a JSON response from the server."""
    data = response.read()
    return json.loads(data).get("message", "Unhandled exception.")
