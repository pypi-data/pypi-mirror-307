"""Timeseer Client provides the low-level connection to Timeseer."""

import base64
import json
import ssl
from dataclasses import dataclass
from datetime import datetime, timezone
from http.client import (
    HTTPConnection as HTTPClientConnection,
)
from http.client import (
    HTTPResponse,
)
from http.client import (
    HTTPSConnection as HTTPSClientConnection,
)
from time import sleep
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import quote as url_quote
from urllib.parse import urljoin, urlsplit, urlunsplit

import pyarrow as pa
from kukur import Metadata, SeriesSearch, SeriesSelector
from kukur.base import SourceStructure

from timeseer_client.internal import (
    ServerReturnedException,
    TooManyRedirectsException,
    TransportException,
    UnauthorizedException,
    parse_json_exception_message,
    parse_json_response,
)
from timeseer_client.internal.flows import (
    evaluate_flow,
    wait_for_flow_evaluation,
)


@dataclass
class TLSOptions:
    """Options for TLS connections.

    Set verify to False to disable certificate validation.

    By default CA certificates of the operating system will be used.
    Alternative certificates can be provided using `root_certs`.
    """

    verify: bool = True
    root_certs: Optional[bytes] = None


HTTPConnection = Union[HTTPClientConnection, HTTPSClientConnection]


class Client:
    """Client connects to Timeseer using HTTP."""

    __context: Optional[ssl.SSLContext] = None
    __use_https: bool = False

    def __init__(
        self,
        api_key: Tuple[str, str] = ("", ""),
        host: str = "localhost",
        port: int = 443,
        use_tls: Optional[Union[bool, TLSOptions]] = None,
    ):
        """Create a new Client.

        Creating a client does not open a connection.

        Args:
            api_key: the api key to use when connecting. This is a tuple of (key name, key).
            host: the hostname where the Timeseer instance is running. Defaults to ``localhost``.
            port: the port where the Timeseer instance is running. Defaults to ``443``.
            use_tls: set to True to use a TLS-secured connection, or pass TLSOptions for more configuration.
        """
        self._host = host
        self._port = port
        self._api_key = api_key
        self._api_prefix = "/public/api/v1/"

        self._tls_options = None
        if (use_tls is None and port == 443) or use_tls is True:
            self._tls_options = TLSOptions()
        elif use_tls:
            self._tls_options = use_tls

        self.__use_https = self._tls_options is not None

        if self._tls_options is not None:
            self.__context = ssl.create_default_context()
            if not self._tls_options.verify:
                self.__context.check_hostname = False
                self.__context.verify_mode = ssl.CERT_NONE
            if self._tls_options.root_certs:
                self.__context.load_verify_locations(
                    cadata=self._tls_options.root_certs
                )

    @classmethod
    def for_tls(
        cls,
        host: str,
        *,
        port: int = 443,
        api_key: Tuple[str, str] = ("", ""),
        tls_options: Optional[TLSOptions] = None,
    ) -> "Client":
        """Create a new Client that uses TLS to secure the connection.

        The CA certificates of the operating system will be used.
        Additional certificates can be provided using `tls_options`.

        Args:
            host: the hostname where Timeseer instance is running.
            port: the port where the Timeseer instance is running. Defaults to ``443``.
            api_key: the api key to use when connecting. This is a tuple of (key name, key).
            tls_options: TLS configuration options.
        """
        use_tls: Union[bool, TLSOptions] = True
        if tls_options is not None:
            use_tls = tls_options
        return cls(
            api_key=api_key,
            host=host,
            port=port,
            use_tls=use_tls,
        )

    def wait_for_available(self, *, timeout: float = 30.0):
        """Wait for the client to be available.

        This will block until the client is available or the timeout is reached.

        Args:
            timeout: the number of seconds to wait for the client to become available.
        """
        while timeout > 0:
            try:
                response = self._heartbeat()
                if response.status in [200, 204]:
                    return
            except Exception:
                pass
            sleep(0.2)
            timeout -= 0.2
        raise TimeoutError("Client did not become available within the timeout.")

    def _heartbeat(self) -> HTTPResponse:
        return self.request("GET", "heartbeat")

    def upload_data(
        self,
        metadata_or_data: Union[Metadata, List[Tuple[Metadata, pa.Table]]],
        table: Optional[pa.Table] = None,
        *,
        analyze=True,
        block=True,
    ):
        """Upload time series data to Timeseer.

        This requires a configured 'flight-upload' source in Timeseer.

        There are two ways to call this method.

        One requires two arguments:
            metadata: any known metadata about the time series. This will be merged with the metadata
                already known by Timeseer depending on the source configuration. The source of the series should match
                the source name of a 'flight-upload' source.
            table: a pyarrow.Table of two columns.
                The first column with name 'ts' contains Arrow timestamps.
                The second column with name 'value' contains the values as a number or string.

        The second accepts a list of tuples of the same arguments. This allows uploading multiple time series at the
        same time.

        When `analyze` is `True`, start a flow evaluation.
        When `block` is `True`, block execution until the flow evaluation is done.
        """
        if table is not None:
            assert isinstance(metadata_or_data, Metadata)
            self._upload_data_single(metadata_or_data, table, analyze, block)
        else:
            assert not isinstance(metadata_or_data, Metadata)
            self._upload_data_multiple(metadata_or_data, analyze, block)

    def search(self, selector: SeriesSearch) -> List[Union[Metadata, SeriesSelector]]:
        """Search Kukur for time series matching the given ``SeriesSelector``.

        Args:
            selector: return time series matching the given selector.
                      Use ``name = None`` (the default) to select all series in a source.

        Returns:
            A generator that returns either ``Metadata`` or ``SeriesSelector``s.
            The return value depends on the search that is supported by the source.
        """
        body = selector.to_data()
        response = self.request(
            "POST",
            "search",
            body=body,
            headers={"Content-type": "Application/JSON"},
        )

        result = []
        for data in parse_json_response(response):
            if "series" not in data:
                result.append(SeriesSelector.from_data(data))
            else:
                result.append(Metadata.from_data(data))
        return result

    def get_metadata(self, selector: SeriesSelector) -> Metadata:
        """Read metadata for the time series selected by the ``SeriesSelector``.

        Args:
            selector: the selected time series

        Returns:
            The ``Metadata`` for the time series.
        """
        body = selector.to_data()
        response = self.request(
            "POST",
            "get-metadata",
            body=body,
        )

        return Metadata.from_data(parse_json_response(response))

    def get_data(
        self,
        selector: SeriesSelector,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> pa.Table:
        """Get raw data for the time series selected by the SeriesSelector.

        Args:
            selector: return data for the time series selected by this selector.
            start_date: the start date of the time range of data to return. Defaults to one year ago.
            end_date: the end date of the time range of data to return. Defaults to now.

        Returns:
            A pyarrow Table with two columns: 'ts' and 'value'.
        """
        start_date, end_date = _apply_default_range(start_date, end_date)
        query = {
            "seriesSelector": selector.to_data(),
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat(),
        }
        return self.do_get(query)

    def list_sources(self) -> List[str]:
        """List all configured sources.

        Returns:
            A list of source names that are configured in Kukur.
        """
        response = self.request(
            "GET",
            "sources/",
        )
        return [source_data["name"] for source_data in parse_json_response(response)]

    def get_source_structure(
        self, selector: SeriesSelector
    ) -> Optional[SourceStructure]:
        """List all tags and fields from a source.

        Returns:
            A list of tag keys, tag values and fields that are configured in the source.
        """
        response = self.request(
            "POST",
            "/public/api/v1/get-source-structure",
            body=selector.to_data(),
        )
        if response.status == 204:
            return None
        response_data = parse_json_response(response)
        return SourceStructure.from_data(response_data)

    def get_plot_data(
        self,
        selector: SeriesSelector,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        interval_count: int = 200,
    ) -> pa.Table:
        """Get plot data for the time series selected by the SeriesSelector.

        Args:
            selector: return data for the time series selected by this selector.
            start_date: the start date of the time range of data to return. Defaults to one year ago.
            end_date: the end date of the time range of data to return. Defaults to now.
            interval_count: the number of intervals included in the plot. Defaults to 200.

        Returns:
            A pyarrow Table with two columns: 'ts' and 'value'.
        """
        start_date, end_date = _apply_default_range(start_date, end_date)
        data = {
            "seriesSelector": selector.to_data(),
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat(),
            "intervalCount": interval_count,
        }
        response = self.request(
            "POST",
            "get-plot-data",
            body=data,
            headers={
                "Accept": "application/vnd.apache.arrow.stream",
            },
        )

        if response.status not in [200, 201]:
            raise ServerReturnedException(parse_json_exception_message(response))
        buffer = response.read()
        reader = pa.ipc.RecordBatchStreamReader(buffer)
        return reader.read_all()

    def do_get(self, data: Any) -> pa.Table:
        """Do an HTTP request to return an Arrow table.

        Args:
            data: The series selector, start and end date of .

        Returns:
            A PyArrow Table.
        """
        response = self.request(
            "POST",
            "get-data",
            body=data,
            headers={
                "Accept": "application/vnd.apache.arrow.stream",
            },
        )

        if response.status not in [200, 201]:
            raise ServerReturnedException(parse_json_exception_message(response))
        buffer = response.read()
        reader = pa.ipc.RecordBatchStreamReader(buffer)
        return reader.read_all()

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
        table = table.replace_schema_metadata({"metadata": json.dumps(data)})
        stream = pa.BufferOutputStream()
        stream_writer = pa.ipc.RecordBatchStreamWriter(stream, table.schema)
        stream_writer.write(table)
        response = self.request(
            "POST",
            "data-upload/upload-data",
            body=stream.getvalue(),
            headers={"content-type": "application/vnd.apache.arrow.stream"},
        )
        if response.status not in [200, 201]:
            raise ServerReturnedException(parse_json_exception_message(response))
        return response

    def request(  # noqa: PLR0913
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        body: Optional[Union[str, Dict[str, Any], pa.Buffer]] = None,
        query: Optional[Dict[str, str]] = None,
    ) -> HTTPResponse:
        """Perform a request to the Timeseer server.

        Args:
            method: the HTTP method to use.
            url: the URL to request.
            headers: optional headers to send.
            body: optional body to send.
            query: optional query parameters to send.

        Returns:
            The response from the server.
        """
        connection = self._get_connection()
        if body is not None and isinstance(body, dict):
            body = json.dumps({"body": body})
            if headers is None or "Content-type" not in headers:
                headers = headers or {}
                headers["Content-type"] = "application/json"
        formatted_url = self._api_prefix + url
        if query is not None and len(query) > 0:
            query_params = [
                f"{url_quote(key)}={url_quote(value)}" for key, value in query.items()
            ]
            formatted_url = f"{formatted_url}?{'&'.join(query_params)}"

        if self._api_key != ("", ""):
            if headers is None:
                headers = {}
            auth = base64.b64encode(
                f"{self._api_key[0]}:{self._api_key[1]}".encode("utf-8")
            )
            headers["Authorization"] = f"Basic {auth.decode()}"

        return _request(connection, method, formatted_url, headers, body)

    def _get_connection(self) -> HTTPConnection:
        if self.__use_https:
            return HTTPSClientConnection(self._host, self._port, context=self.__context)
        return HTTPClientConnection(self._host, self._port)

    def _upload_data_single(
        self, metadata: Metadata, table: pa.Table, analyze: bool, block: bool
    ):
        self._upload_data_multiple([(metadata, table)], analyze, block)

    def _upload_data_multiple(
        self, many_series: List[Tuple[Metadata, pa.Table]], analyze: bool, block: bool
    ):
        selectors = []
        for metadata, table in many_series:
            metadata_json = metadata.to_data()
            selector = SeriesSelector.from_tags(
                metadata.series.source, metadata.series.tags, metadata.series.field
            )
            selectors.append(selector)
            response = self.do_put(metadata_json, table)
            response_data = parse_json_response(response)

        if "flowName" in response_data:
            if analyze:
                evaluate_flow(
                    self, response_data["flowName"], limitations=selectors, block=block
                )
        if block and "flowEvaluationGroupId" in response_data:
            wait_for_flow_evaluation(self, response_data)


def _request(  # noqa: PLR0913
    connection: HTTPConnection,
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    body: Optional[Union[str, Dict[str, Any], pa.Buffer]] = None,
    redirect_count=0,
) -> HTTPResponse:
    kwargs: dict[str, Any] = {}
    if headers is not None:
        kwargs["headers"] = headers
    if body is not None:
        kwargs["body"] = body
    connection.request(method, url, **kwargs)
    response = connection.getresponse()
    location_header = response.getheader("location")
    if location_header is None:
        if response.status == 401:
            raise UnauthorizedException()
        if response.status not in [200, 201, 204]:
            if "application/json" in response.getheader("Content-Type", ""):
                raise ServerReturnedException(parse_json_exception_message(response))
            raise TransportException(response.status, response.read().decode("utf-8"))
        return response

    redirect_count = redirect_count + 1
    if redirect_count > 5:
        raise TooManyRedirectsException(
            f"Too many redirects ({redirect_count}) to {location_header}"
        )

    response.read()
    location_parts = urlsplit(urljoin(url, location_header))._replace(
        scheme="", netloc=""
    )
    location = urlunsplit(location_parts)

    return _request(connection, method, location, headers, body, redirect_count)


def _apply_default_range(
    start_date: Optional[datetime], end_date: Optional[datetime]
) -> Tuple[datetime, datetime]:
    if start_date is None or end_date is None:
        now = datetime.now(tz=timezone.utc)
        if start_date is None:
            start_date = now.replace(year=now.year - 1)
        if end_date is None:
            end_date = now
    return start_date, end_date
