from __future__ import annotations

from typing import List, TypedDict

 

from  webdock.webdock.events import EventType

 
from  webdock.webdock.req  import RequestOptions, req
 
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from webdock import Webdock




class HookFilter(TypedDict):
    type: str
    value: str


class Hook(TypedDict):
    id: int
    callbackUrl: str
    filters: List[HookFilter]


class GetHookByIdResponseType(TypedDict):
    body: Hook


class ListHooksResponseType(TypedDict):
    body: List[Hook]


class Hooks:
    def __init__(self, parent: "Webdock") -> None:
        self.parent = parent

    def getById(self, *, id: int) -> GetHookByIdResponseType:
        return req(
            RequestOptions(
                endpoint=f"hooks/{id}",
                method="GET",
                token=self.parent.string_token,
            )
            
        )

    def create(self, *, callbackUrl: str, eventType: EventType | None = None, callbackId: int | None = None) -> GetHookByIdResponseType:
        return req(
            RequestOptions(
                endpoint="/hooks",
                method="POST",
                token=self.parent.string_token,
                body={
                    "callbackUrl": callbackUrl,
                    "callbackId": callbackId,
                    "eventType": eventType,
                },
            )
         )

    def deleteById(self, *, id: int):
        return req(
            RequestOptions(
                endpoint=f"hooks/{id}",
                method="DELETE",
                token=self.parent.string_token,
            )
        )

    def list(self) -> ListHooksResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint="/hooks",
                method="GET",
            )
        )


