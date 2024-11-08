"""Python client for Timeseer Sources."""

import time

from timeseer_client.internal import TimeseerClient, parse_json_response


class Sources:
    """Sources provide access to timeseries and metadata.

    Args:
        client: the Timeseer Client
    """

    __client: TimeseerClient

    def __init__(self, client: TimeseerClient):
        self.__client = client

    def update(self, source_name: str, *, block=True):
        """Update a source.

        Args:
            source_name: the name of the source to analyze
            block: block until the update completes (keyword-only, default True)
        """
        self.__client.request(
            "POST", "sources/update", query={"sourceName": source_name}
        )

        if block:
            self.wait_for_update(source_name)

    def wait_for_update(self, source_name: str):
        """Wait until the metadata update of the given source completes.

        Args:
            source_name: the name of the source to analyze
        """
        while True:
            response = self.__client.request(
                "GET", "sources/update", query={"sourceName": source_name}
            )
            state = parse_json_response(response)
            if state["completed"] == state["total"]:
                break
            time.sleep(0.2)
