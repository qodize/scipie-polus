import dataclasses
import datetime as dt
from typing import Tuple, Optional


@dataclasses.dataclass
class User:
    phone: str


@dataclasses.dataclass
class Driver:
    phone: str


@dataclasses.dataclass
class Transport:
    type: str


@dataclasses.dataclass
class Order:
    user: User
    driver: Optional[Driver]
    transport: Transport
    start: dt.datetime
    end: dt.datetime
    geodata: Tuple[float]

