from __future__ import annotations

from typing import List, Literal, TypedDict, Optional

 
from  webdock.webdock.req  import RequestOptions, req
 
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from webdock import Webdock


ServerStatus = Literal[
    "provisioning",
    "running", 
    "stopped",
    "error",
    "rebooting",
    "starting",
    "stopping",
    "reinstalling",
    "suspended"
]

VirtualizationType = Literal["container", "kvm"]
ServerType = Literal["Apache", "Nginx", "None"]


 
class Server(TypedDict):
    slug: str
    name: str
    date: str
    location: str
    image: str
    profile: str
    ipv4: str | None
    ipv6: str | None
    status: ServerStatus
    virtualization: VirtualizationType
    webServer: ServerType
    aliases: List[str]
    snapshotRunTime: int
    description: str
    WordPressLockDown: bool
    SSHPasswordAuthEnabled: bool
    notes: str
    nextActionDate: str

class CallBackHeader(TypedDict):
    x_callback_id: str

    
class CreateServerResponseType(TypedDict):
    body: Server
    headers: CallBackHeader

    
class GetServerResponseType(TypedDict):
    body: Server

class DeleteServerResponseType(TypedDict):
    body: Server
    headers: CallBackHeader


class FetchFileResponsePayload(TypedDict):
    body: dict
    headers: CallBackHeader


class ListServersResponseType(TypedDict):
    body: List[Server]


class ReinstallServerResponseType(TypedDict):
    body: Server
    headers: CallBackHeader


class WarningDTO(TypedDict):
    type: str
    message: str
    data: dict[str, str | int]


class Price(TypedDict):
    amount: int
    currency: Literal["EUR", "DKK", "USD"]


class ChargeSummaryItemDTO(TypedDict):
    text: str
    price: Price
    isRefund: bool


class ChargeSummaryTotalDTO(TypedDict):
    subTotal: Price
    vat: Price
    total: Price


class ChargeSummaryDTO(TypedDict):
    items: List[ChargeSummaryItemDTO]
    total: ChargeSummaryTotalDTO


class DryRunResponse(TypedDict):
    warnings: List[WarningDTO]
    chargeSummary: ChargeSummaryDTO


class ResizeDryRunResponseType(TypedDict):
    body: DryRunResponse


class ResizeResponseType(TypedDict):
    body: Server
    headers: CallBackHeader


class StartResponseType(TypedDict):
    body: Server
    headers: CallBackHeader


class ArchiveResponseType(TypedDict):
    body: Server
    headers: CallBackHeader


class UpdateServerResponseType(TypedDict):
    body: Server


class MetricsSamplingDTO(TypedDict):
    amount: int
    timestamp: str


class DiskMetricsDTO(TypedDict):
    allowed: int
    samplings: List[MetricsSamplingDTO]


class NetworkMetricsDTO(TypedDict):
    total: int
    allowed: int
    ingressSamplings: List[MetricsSamplingDTO]
    egressSamplings: List[MetricsSamplingDTO]


class CpuMetricsDTO(TypedDict):
    usageSamplings: List[MetricsSamplingDTO]


class ProcessesMetricsDTO(TypedDict):
    processesSamplings: List[MetricsSamplingDTO]


class MemoryMetricsDTO(TypedDict):
    usageSamplings: List[MetricsSamplingDTO]


class MetricsNowResponseType(TypedDict):
    body: dict


class Servers:
    def __init__(self, parent: "Webdock") -> None:
        self.parent = parent

    def create(
        self,
        *,
        name: str,
        locationId: str,
        profileSlug: Optional[str] = None,
        imageSlug: Optional[str] = None,
        virtualization: Optional[str] = None,
        slug: Optional[str] = None,
        snapshotId: Optional[int] = None,
    ) -> CreateServerResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint="/servers",
                method="POST",
                body={
                    "name": name,
                    "locationId": locationId,
                    "profileSlug": profileSlug,
                    "imageSlug": imageSlug,
                    "virtualization": virtualization,
                    "slug": slug,
                    "snapshotId": snapshotId,
                },
                headers=["X-Callback-ID"],
            ),
            
        )

    def delete(self, *, serverSlug: str) -> DeleteServerResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/servers/{serverSlug}",
                method="DELETE",
                headers=["X-Callback-ID"],
            ),
            
        )

    def fetchFile(self, *, path: str, slug: str) -> FetchFileResponsePayload:
        return req(
            RequestOptions(
                endpoint=f"servers/{slug}/fetchFile",
                method="POST",
                token=self.parent.string_token,
                body={"filePath": path},
                headers=["X-Callback-ID"],
            ),
            
        )

    def getBySlug(self, *, serverSlug: str) -> GetServerResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/servers/{serverSlug}",
                method="GET",
            ),
            
        )

    def list(self) -> ListServersResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint="/servers",
                method="GET",
            ),
            
        )

    def metricsNow(self, *, serverSlug: str, now: bool) -> MetricsNowResponseType:
        endpoint = f"servers/{serverSlug}/metrics"
        if now:
            endpoint += "/now"
        
        return req(
            RequestOptions(
                endpoint=endpoint,
                method="GET",
                token=self.parent.string_token,
            ),
            
        )

    def reboot(self, *, serverSlug: str)->StartResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/servers/{serverSlug}/actions/reboot",
                method="POST",
                headers=["X-Callback-ID"],
            ),
            
        )

    def reinstall(self, *, imageSlug: str, serverSlug: str) -> ReinstallServerResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/servers/{serverSlug}/actions/reinstall",
                method="POST",
                body={"imageSlug": imageSlug},
                headers=["X-Callback-ID"],
            ),
            
        )

    def resize(self, *, serverSlug: str, profileSlug: str) -> ResizeResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/servers/{serverSlug}/actions/resize",
                method="POST",
                body={"profileSlug": profileSlug},
                headers=["X-Callback-ID"],
            ),
            
        )

    def resizeDryRun(self, *, serverSlug: str, profileSlug: str) -> ResizeDryRunResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/servers/{serverSlug}/actions/resize/dryrun",
                method="POST",
                body={"profileSlug": profileSlug},
            ),
            
        )

    def start(self, *, serverSlug: str) -> StartResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/servers/{serverSlug}/actions/start",
                method="POST",
                headers=["X-Callback-ID"],
            ),
            
        )

    def stop(self, *, serverSlug: str) -> StartResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/servers/{serverSlug}/actions/stop",
                method="POST",
                headers=["X-Callback-ID"],
            ),
            
        )

    def archive(self, *, serverSlug: str) -> ArchiveResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/servers/{serverSlug}/actions/suspend",
                method="POST",
                headers=["X-Callback-ID"],
            ),
            
        )

    def update(
        self,
        *,
        serverSlug: str,
        nextActionDate: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> UpdateServerResponseType:
        return req(
            RequestOptions(
                token=self.parent.string_token,
                endpoint=f"/servers/{serverSlug}",
                method="PATCH",
                body={
                    "nextActionDate": nextActionDate,
                    "name": name,
                    "description": description,
                    "notes": notes,
                },
            ),
            
        )