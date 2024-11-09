from __future__ import annotations

from typing import List, Optional

from ..resource import Resource
from ...schemas import (
    Characterization,
    Backend as BackendSchema,
)


class BackendsResource(Resource):

    def get_backends(self, status: Optional[str] = None) -> List[BackendSchema]:
        params = {"status": status} if status is not None else {}
        response = self.client.request(
            "/backends",
            method="GET",
            params=params,
        )
        assert isinstance(response, list), "Get Backends response is not a list"
        return [BackendSchema(**backend) for backend in response]

    def get_characterizations(
        self,
        backend: str,
        start: Optional[int] = None,
        end: Optional[int] = None,
        limit: int = 10,
        page: int = 1,
    ) -> List[Characterization]:
        assert backend is not None, "Backend name is required"
        params = {"start": start, "end": end, "limit": limit, "page": page}
        response = self.client.request(
            f"/characterizations/backends/{backend}",
            method="GET",
            params=params,
        )
        assert isinstance(
            response, dict
        ), "Get Characterizations response is not a dict"
        return [
            Characterization(**char) for char in response.get("characterizations", [])
        ]

    def get_current_characterization(self, backend: str) -> Characterization:
        assert backend is not None, "Backend name is required"
        response = self.client.request(
            f"/characterizations/backends/{backend}/current",
            method="GET",
        )
        assert isinstance(
            response, dict
        ), "Get Current Characterization response is not a dict"
        return Characterization(**response)

    def get_characterization(self, uuid: str) -> Characterization:
        response = self.client.request(
            f"/characterizations/{uuid}",
            method="GET",
        )
        assert isinstance(response, dict), "Get Characterization response is not a dict"
        return Characterization(**response)
