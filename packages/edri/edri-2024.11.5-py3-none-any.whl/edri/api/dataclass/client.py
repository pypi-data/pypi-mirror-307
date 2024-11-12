from multiprocessing.connection import Connection
from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class Client:
    socket: Connection
