from __future__ import annotations

from typing import Literal, TypedDict

 
from  webdock.webdock.req  import RequestOptions, req
 
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from webdock import Webdock




class AccountInformation(TypedDict):
    userId: int
    companyName: str
    userName: str
    userAvatar: str
    userEmail: str
    isTeamMember: bool
    teamLeader: str
    accountBalance: str
    accountBalanceRaw: str
    accountBalanceCurrency: str


class AccountInformationReturnType(TypedDict):
    body: AccountInformation


class Account:
    def __init__(self, parent: "Webdock") -> None:
        self.parent = parent

    def info(self) -> AccountInformationReturnType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint="/account/accountInformation",
                method="GET",
                headers=[],
            )
            
        )


