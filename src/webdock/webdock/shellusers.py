from __future__ import annotations

from typing import List, Optional, TypedDict


 
from  webdock.webdock.req  import RequestOptions, req
 
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from webdock import Webdock


class ShellUser(TypedDict):
    id: int
    username: str
    group: str
    shell: str
    created: str
    updated: str
    publicKeys: List[int]

class CallBackHeader(TypedDict):
    x_callback_id: str

class ShellUserDTO(TypedDict):
    id: int
    username: str
    group: str
    shell: str
    publicKeys: List[dict]
    created: str


class ListShellUserDTO(TypedDict):
    id: int
    username: str
    group: str
    shell: str
    publicKeys: List[dict]
    created: str


class CreateShellUserResponseType(TypedDict):
    body: ShellUserDTO
    headers: CallBackHeader


class DeleteUserShellResponseType(TypedDict):
    body: ShellUser
    headers: CallBackHeader


class ListShellUsersResponseType(TypedDict):
    body: List[ShellUser]

class TokenBody(TypedDict):
    token: str
class CreateWebSSHTokenResponseType(TypedDict):
    body: TokenBody


class ShellUsers:
    def __init__(self, parent: "Webdock") -> None:
        self.parent = parent

    def create(
        self,
        *,
        serverSlug: str,
        username: str,
        password: str,
        group: Optional[str] = None,
        shell: Optional[str] = None,
        publicKeys: Optional[List[int]] = [],
    ) -> CreateShellUserResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"servers/{serverSlug}/shellUsers",
                method="POST",
                body={
                    "username": username,
                    "password": password,
                    "group": group,
                    "shell": shell,
                    "publicKeys": publicKeys or [],
                },
                headers=["X-Callback-ID"],
            ),
            
        )

    def delete(self, *, serverSlug: str, userId: int) -> DeleteUserShellResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"servers/{serverSlug}/shellUsers/{userId}",
                method="DELETE",
                headers=["X-Callback-ID"],
            ),
            
        )

    def list(self, *, serverSlug: str) -> ListShellUsersResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/servers/{serverSlug}/shellUsers",
                method="GET",
            ),
            
        )

    def edit(self, *, slug: str, id: int, keys: List[int] = []) -> CreateShellUserResponseType:
        return req(
            RequestOptions(
                endpoint=f"servers/{slug}/shellUsers/{id}",
                method="PATCH",
                body={"publicKeys": keys},
                headers=["X-Callback-ID"],
                token=self.parent.string_token,
            ),
            
        )

    def websshToken(self, *, serverSlug: str, username: str) -> CreateWebSSHTokenResponseType:
        return req(
            RequestOptions(
                endpoint=f"servers/{serverSlug}/shellUsers/WebsshToken",
                method="POST",
                token=self.parent.string_token,
                body={"username": username},
            ),
        
        )


