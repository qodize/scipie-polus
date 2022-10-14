import dataclasses
import datetime as dt
from typing import Tuple, Optional


@dataclasses.dataclass
class User:
    id: int
    phone: str


@dataclasses.dataclass
class Driver:
    id: int
    phone: str


@dataclasses.dataclass
class Transport:
    type: str


@dataclasses.dataclass
class Order:
    id: Optional[int]
    user: User
    driver: Optional[Driver]
    transport: Transport
    start: dt.datetime
    end: dt.datetime
    latitude: float
    longitude: float
    status: str

    @classmethod
    def from_json(cls, data):
        user = User(**data.pop('user'))
        driver = Driver(**data.pop('driver')) if data.get('driver') else None
        transport = Transport(**data.pop('transport'))
        return cls(id=data.pop('id', None), user=user, driver=driver, transport=transport, **data)
