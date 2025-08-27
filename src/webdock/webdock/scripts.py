from __future__ import annotations

from typing import List, Literal, TypedDict


 
from  webdock.webdock.req  import RequestOptions, req
 
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from webdock import Webdock



class CreateScriptBodyType(TypedDict):
    name: str
    filename: str
    content: str


class CreateScriptResponseType(TypedDict):
    body: Script

class ResponseHeaders(TypedDict):
    x_callback_id: str


class Script(TypedDict):
    id: int
    name: str
    path: str
    lastRun: str | None
    lastRunCallbackId: str | None
    created: str

class GetScriptResponse(TypedDict):
    body: Script

class CreateScriptOnServerResponse(TypedDict):
    headers: ResponseHeaders
    body: Script

class DeleteScriptOnServerResponse(TypedDict):
    headers: ResponseHeaders

class ExecuteScriptOnServerResponse(TypedDict):
    headers: ResponseHeaders
 


class ListScriptsOnServerResponseType(TypedDict):
    body: List[Script]


class ListScriptsResponseType(TypedDict):
    body: List[dict]

class UpdateAccountScriptResponseType(TypedDict):
    body: Script

class Scripts:
    def __init__(self, parent: "Webdock") -> None:
        self.parent = parent

    def createAccountScript(self, *, name: str, filename: str, content: str) -> CreateScriptResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint="/account/scripts",
                method="POST",
                body={"content": content, "filename": filename, "name": name},
            ),
            
        )

    def deployAccountScriptOnServer(
        self,
        *,
        scriptId: int,
        path: str,
        makeScriptExecutable: bool,
        executeImmediately: bool,
        serverSlug: str,
    ) -> CreateScriptOnServerResponse:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/servers/{serverSlug}/scripts",
                method="POST",
                body={
                    "scriptId": scriptId,
                    "path": path,
                    "makeScriptExecutable": makeScriptExecutable,
                    "executeImmediately": executeImmediately,
                },
                headers=["X-Callback-ID"],
            ),
            
        )

    def deleteAccountScript(self, *, id: int) -> None:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/account/scripts/{id}",
                method="DELETE",
            ),
            
        )

    def deleteScriptFromServer(self, *, serverSlug: str, scriptId: int) -> DeleteScriptOnServerResponse:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/servers/{serverSlug}/scripts/{scriptId}",
                method="DELETE",
                headers=["X-Callback-ID"],
            ),
            
        )

    def executeOnServer(self, *, serverSlug: str, scriptID: int) -> ExecuteScriptOnServerResponse:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/servers/{serverSlug}/scripts/{scriptID}/execute",
                method="POST",
                headers=["X-Callback-ID"],
            ),
            
        )

    def getAccountScriptById(self, *, scriptId: int) -> GetScriptResponse:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/account/scripts/{scriptId}",
                method="GET",
            ),
            
        )

    def listAccountScripts(self) -> ListScriptsResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint="/account/scripts",
                method="GET",
            ),
            
        )

    def listServerScripts(self, *, serverSlug: str) -> ListScriptsOnServerResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/servers/{serverSlug}/scripts",
                method="GET",
            ),
            
        )


    def updateAccountScript(self, *, id: int, name: str, filename: str, content: str) -> UpdateAccountScriptResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/account/scripts/{id}",
                method="PATCH",
                body={"name": name, "filename": filename, "content": content},
            ),
            
        )


