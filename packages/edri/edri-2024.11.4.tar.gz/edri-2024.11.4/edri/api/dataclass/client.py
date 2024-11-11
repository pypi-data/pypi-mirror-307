from multiprocessing.connection import Connection
from dataclasses import dataclass, field

from edri.config.constant import ApiType


@dataclass(frozen=True, eq=True)
class Client:
    socket: Connection
    type: ApiType
