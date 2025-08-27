from __future__ import annotations

from typing import List, Literal, TypedDict
 
from  webdock.webdock.req  import RequestOptions, req
 
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from webdock import Webdock


class EventLog(TypedDict):
    id: int
    startTime: str
    endTime: str | None
    callbackId: str
    serverSlug: str
    eventType: str
    action: str
    actionData: str
    status: Literal["waiting", "working", "finished", "error"]
    message: str


class EventLogResponse(TypedDict):
    body: List[EventLog]


class Operation:
    def __init__(self, parent: "Webdock") -> None:
        self.parent = parent

    def fetch(self, callbackId: str) -> EventLogResponse:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/events?callbackId={callbackId}",
                method="GET",
            )
        )


