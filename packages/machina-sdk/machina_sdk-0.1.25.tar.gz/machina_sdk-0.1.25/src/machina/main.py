from machina.resources.http_client import HttpClient

from machina.resources import (
    Organization,
    Project
)


class Machina:
    """"""

    def __init__(
        self,
        api_key: str | None = None,
        api_url: str | None = None,
    ):
        """"""

        if api_key is None:
            raise ValueError("Value api_key must be set.")

        if api_url is None:
            raise ValueError("Value api_url must be set.")

        self.api_key = api_key

        self.api_url = api_url

        self.api = HttpClient(self.api_key)

        self.organization = Organization(client=self.api)

        self.project = Project(client=self.api)

        print("[ ::: Machina SDK initialized! ::: ]")


__all__ = [
    'Machina'
]
