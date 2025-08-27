from __future__ import annotations

from typing import List, TypedDict


 
from  webdock.webdock.req  import RequestOptions, req
 
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from webdock import Webdock



class SSHKeys(TypedDict):
    fingerprint: str
    id: int
    name: str
    key: str
    created: str


class CreateSSHKeysResponseType(TypedDict):
    body: SSHKeys


class ListSSHKeysResponseType(TypedDict):
    body: List[SSHKeys]
class CallBackHeader(TypedDict):
    x_callback_id: str


class SshKeys:
    def __init__(self, parent: "Webdock") -> None:
        self.parent = parent

    def create(self, *, name: str, publicKey: str) -> CreateSSHKeysResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint="/account/publicKeys",
                method="POST",
                body={"name": name, "publicKey": publicKey},
            ),
            
        )

    def delete(self, *, id: int) -> None:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/account/publicKeys/{id}",
                method="DELETE",
                headers=["X-Callback-ID"]
            ),
        )

    def list(self) -> ListSSHKeysResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint="/account/publicKeys",
                method="GET",
            ),
            
        )


