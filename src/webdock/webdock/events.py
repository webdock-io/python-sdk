from __future__ import annotations

from typing import List, Literal, Optional, TypedDict 

 
 
from  webdock.webdock.req  import RequestOptions, req
 
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from webdock import Webdock


EventType = Literal["provision",
"restore-server",
"change-profile",
"set-state",
"delete",
"backup",
"set-hostnames",
"update-webroot",
"setup-ssl",
"install-wordpress",
"manage-wordpress",
"manage-shelluser",
"manage-keys",
"toggle-passwordauth",
"manage-mysql",
"manage-dbuser",
"manage-ftpuser",
"set-php-settings",
"cronjob",
"pull-file",
"push-file",
"delete-file",
"execute-file"]

EventStatus = Literal["waiting", "working", "finished", "error"]


class EventsType(TypedDict):
    id: int
    startTime: str
    endTime: Optional[str | None]
    callbackId: str
    serverSlug: str
    eventType: EventType
    action: str
    actionData: str
    message: str
    status: EventStatus


class EventTypeListResponse(TypedDict):
    body: List[EventsType]


class Events:
    def __init__(self, parent: "Webdock") -> None:
        self.parent = parent

    def list(self, *, page: int = 1, limit: int = 10, type: str = "") -> EventTypeListResponse:
        endpoint = "/events"
        query_params: list[str] = []

        if page:
            query_params.append(f"page={page}")
        if limit:
            query_params.append(f"per_page={limit}")
        if type:
            query_params.append(f"eventType={type}")

        if query_params:
            endpoint += "?" + "&".join(query_params)

        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=endpoint,
                headers=["x-total-count"],
                method="GET",
            )
            
        )


