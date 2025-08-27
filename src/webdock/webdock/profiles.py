from __future__ import annotations

from typing import List, TypedDict



 
from  webdock.webdock.req  import RequestOptions, req
 
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from webdock import Webdock



class CPU:
    cores: int
    threads: int


class Price:
    amount: int
    currency: str


class Profile:
    slug: str
    name: str
    ram: int
    disk: int
    cpu: CPU
    price: Price


class ListProfilesResponseType(TypedDict):
    body: List[Profile]


class Profiles:
    def __init__(self, parent: "Webdock") -> None:
        self.parent = parent

    def list(self, *, locationId: str = "dk", profileSlug: str = "") -> ListProfilesResponseType:
        res = req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/profiles?locationId={locationId}&profileSlug={profileSlug}",
                method="GET",
            )
        )
 
        return res


