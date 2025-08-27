from __future__ import annotations

from typing import List, TypedDict
 
from  webdock.webdock.req  import RequestOptions, req
 
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from webdock import Webdock


class Location(TypedDict):
    id: str
    name: str
    city: str
    country: str
    description: str
    icon: str


class ListLocationsType(TypedDict):
    body: List[Location]


class Locations:
    def __init__(self, parent: "Webdock") -> None:
        self.parent = parent

    def list(self) -> ListLocationsType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint="/locations",
                method="GET",
            )
        )


