"""Python client for Timeseer Flows."""

import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from kukur import SeriesSelector

from timeseer_client.internal import (
    TimeseerClient,
    TimeseerClientException,
    parse_json_response,
)


class FlowEvaluationFailedException(TimeseerClientException):
    """Thrown when a flow evaluation fails."""

    def __init__(self, flow_name: Optional[str]):
        if flow_name is None:
            super().__init__("flow evaluation failed.")
        else:
            super().__init__(f'evaluation for flow "{flow_name}" failed.')


class Flows:
    """Flows run modules to process time series data.

    Args:
        client: the Timeseer Client
    """

    __client: TimeseerClient

    def __init__(self, client: TimeseerClient):
        self.__client = client

    def list(self) -> List[str]:
        """Return a list containing all the flow names."""
        response = self.__client.request("GET", "flows/")
        return [flow["name"] for flow in parse_json_response(response)]

    def evaluate(self, flow_name: str, *, block=True):
        """Evaluate a flow.

        Args:
            flow_name: the name of the flow to evaluate
            block: block until the evaluation completes (keyword-only, default True)

        Raises:
            FlowEvaluationFailedException when a failure is reported.
        """
        evaluate_flow(self.__client, flow_name, block=block)

    def duplicate(  # noqa: PLR0913
        self,
        existing_flow_name: str,
        new_flow_name: str,
        *,
        series_set_names: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        data_set_name: Optional[str] = None,
    ):
        """Duplicate an existing flow.

        Args:
            existing_flow_name: the name of the flow to duplicate.
            new_flow_name: the name of the duplicated flow.
            series_set_names: the names of the existing series sets to be used in the flow. (Optional).
            start_date: the start date of the flow (Optional).
            end_date: the end date of the flow (Optional).
            data_set_name: the name of the data set to use for the flow (Optional).
        """
        body: Dict[str, Any] = {
            "name": existing_flow_name,
            "newFlowName": new_flow_name,
        }
        if series_set_names is not None:
            body["seriesSetNames"] = series_set_names
        if start_date is not None:
            body["startDate"] = start_date.isoformat()
        if end_date is not None:
            body["endDate"] = end_date.isoformat()
        if data_set_name is not None:
            body["dataSetName"] = data_set_name
        self.__client.request(
            "POST",
            "flows/duplicate",
            body=body,
        )


def evaluate_flow(
    client: TimeseerClient,
    flow_name: str,
    *,
    limitations: Optional[List[SeriesSelector]] = None,
    block=True,
):
    """Trigger an evaluation of the flow with the given name."""
    body: Dict = {"name": flow_name}
    if limitations is not None:
        body["limitations"] = [selector.to_data() for selector in limitations]
    http_response = client.request(
        "POST",
        "flows/evaluate",
        body=body,
    )
    response = parse_json_response(http_response)
    if block:
        wait_for_flow_evaluation(client, response, flow_name)


def wait_for_flow_evaluation(
    client: TimeseerClient, response: Dict, flow_name: Optional[str] = None
):
    """Repeatedly query for the flow evaluation state of the given flow evaluation group."""
    while True:
        http_response = client.request(
            "POST",
            "flows/evaluate/group/state",
            body=response,
        )
        state = parse_json_response(http_response)
        if state["completed"] == state["total"]:
            if state["failed"] > 0:
                raise FlowEvaluationFailedException(flow_name)
            break
        time.sleep(0.2)
