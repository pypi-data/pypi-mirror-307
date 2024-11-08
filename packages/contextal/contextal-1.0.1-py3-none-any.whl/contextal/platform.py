"""
Platform interface and related classes
"""

import json
import logging
import typing

import requests

from contextal import __version__
from contextal.config import Config


LOG = logging.getLogger(__name__)


class QueryError(Exception):
    """Query failure"""

    def __init__(self, error_type, error_message):
        super().__init__(self, error_type)
        super().add_note(error_message)


class ScenarioDuplicateNameError(Exception):
    """The name of the new scenario clashes with an existing one"""


class ScenarioReplacementError(Exception):
    """The scenario to be replaced no longer exists"""


class Platform:
    """Platform interface"""

    def __init__(self, config: Config):
        self.url, self.token = config.platform()
        self.ses = requests.Session()

    def _send_request(
        self,
        api,
        method,
        **kwargs,
    ) -> requests.Response:
        url = self.url + api
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"]["User-Agent"] = "Ctx/" + __version__
        if self.token:
            kwargs["headers"]["Authorization"] = "Bearer " + self.token
        response = self.ses.request(method, url, **kwargs)
        LOG.debug(
            "Request for %s => %s: %s", api, response.status_code, response.headers
        )
        return response

    def submit_work(
        self,
        object_stream: typing.BinaryIO,
        object_name: str | None = None,
        ttl: int | None = None,
        max_recursion: int | None = None,
        org: str | None = None,
    ) -> dict:
        """Submit an object for processing"""
        files = {"object_data": object_stream}
        if object_name:
            files["relation_metadata"] = (
                None,
                json.dumps({"name": object_name}),
                "application/json",
            )
        data = {"ttl": ttl, "maxrec": max_recursion, "org": org}
        response = self._send_request("/api/v1/submit", "POST", files=files, data=data)
        response.raise_for_status()
        return response.json()

    def get_graphs(self, work_ids: list[str]) -> dict:
        """Retrieve graphs for the selected work ids"""
        response = self._send_request(
            "/api/v1/get_works_graphs", "POST", json={"work_ids": work_ids}
        )
        response.raise_for_status()
        return response.json()

    def get_actions(self, work_id: str, max_items: int = None) -> list[dict]:
        """Retrieve scenario actions for the selected work id"""
        api = "/api/v1/actions/" + work_id
        if max_items is not None:
            api += "?maxitems={0}".format(max_items)
        response = self._send_request(api, "GET")
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _handle_query_response(response):
        if response.status_code == 400:
            try:
                err = response.json()
                raise QueryError(err["kind"], err["message"])
            except QueryError:
                raise
            except Exception:
                pass
        response.raise_for_status()
        return response.json()

    def search(self, query: str, get_objects: bool, max_items: int = None) -> list[str]:
        """Execute queries on the platform"""
        data = {
            "q": query,
            "getobjects": get_objects,
        }
        if max_items is not None:
            data["maxitems"] = max_items
        response = self._send_request("/api/v1/search", "POST", json=data)
        return self._handle_query_response(response)

    def count(self, query: str, get_objects: bool) -> list[str]:
        """Execute queries on the platform counting (rather than returning) matches"""
        data = {
            "q": query,
            "getobjects": get_objects,
        }
        response = self._send_request("/api/v1/count", "POST", json=data)
        return self._handle_query_response(response)

    def add_scenario(self, scenario: dict, replace_id: int | None = None) -> dict:
        """Add or replace a scenario"""
        api = "/api/v1/scenarios"
        if replace_id is not None:
            api += "?replace_id=" + str(replace_id)
        response = self._send_request(api, "POST", json=scenario)
        if response.status_code == 409:
            raise ScenarioDuplicateNameError()
        if response.status_code == 404:
            raise ScenarioReplacementError()
        response.raise_for_status()
        return response.json()

    def delete_scenario(self, scenario_id: int):
        """Delete a scenario"""
        api = "/api/v1/scenarios/" + str(scenario_id)
        response = self._send_request(api, "DELETE")
        response.raise_for_status()

    def list_scenarios(self) -> list[dict]:
        """List scenarios"""
        response = self._send_request("/api/v1/scenarios", "GET")
        response.raise_for_status()
        return response.json()

    def get_scenario(self, scenario_id: int) -> dict:
        """Retrieve a scenario"""
        api = "/api/v1/scenarios/" + str(scenario_id)
        response = self._send_request(api, "GET")
        response.raise_for_status()
        return response.json()

    def reload_scenarios(self):
        """Trigger a reload of the existing scenarios"""
        response = self._send_request("/api/v1/scenarios/reload", "POST")
        response.raise_for_status()

    def apply_scenarios(self, work_ids: list[str]):
        """Trigger the (re-)application of scenarios to the specified works"""
        response = self._send_request("/api/v1/scenarios/apply", "POST", json={"work_ids": work_ids})
        response.raise_for_status()

    def download_object(self, object_id: str) -> requests.Response:
        """Attempt to download object data"""
        api = "/api/v1/get_object/" + object_id
        response = self._send_request(api, "GET", stream=True)
        response.raise_for_status()
        return response
