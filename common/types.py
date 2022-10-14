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
    user_id: int
    driver_id: Optional[int]
    transport_type: str
    start: dt.datetime
    end: dt.datetime
    latitude: float
    longitude: float
    status: Optional[str]

    @classmethod
    def from_json(cls, data):
        data['start'] = dt.datetime.fromisoformat(data['start'])
        data['end'] = dt.datetime.fromisoformat(data['end'])
        data['id'] = data.get('id', None)
        data['driver_id'] = data.get('driver_id', None)
        data['status'] = data.get('status', None)
        return cls(**data)

    def to_json(self):
        data = self.__dict__
        return data
