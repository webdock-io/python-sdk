from  webdock.webdock.account import Account
from  webdock.webdock.events import Events
from  webdock.webdock.hooks import Hooks
from  webdock.webdock.images import Images
from  webdock.webdock.locations import Locations
from  webdock.webdock.profiles import Profiles
from  webdock.webdock.scripts import Scripts
from  webdock.webdock.servers import Servers
from  webdock.webdock.shellusers import ShellUsers
from  webdock.webdock.sshkeys import SshKeys
from  webdock.webdock.snapshots import Snapshots
from  webdock.webdock.operation import Operation


class Webdock:
    def __init__(self, token: str) -> None:
        self.string_token: str = token
        self.account: Account = Account(self)
        self.images: Images = Images(self)
        self.profiles: Profiles = Profiles(self)
        self.events: Events = Events(self)
        self.hooks: Hooks = Hooks(self)
        self.locations: Locations = Locations(self)
        self.scripts: Scripts = Scripts(self)
        self.servers: Servers = Servers(self)
        self.shellUsers: ShellUsers = ShellUsers(self)
        self.sshkeys: SshKeys = SshKeys(self)
        self.snapshots: Snapshots = Snapshots(self)
        self.operation: Operation = Operation(self)


# Export the main class for easy importing
__all__ = ['Webdock']
