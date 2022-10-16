import dataclasses
import datetime as dt
from typing import Tuple, Optional


@dataclasses.dataclass
class User:
    id: Optional[int]
    phone: str


@dataclasses.dataclass
class Driver:
    id: Optional[int]
    phone: str

    def to_json(self):
        return self.__dict__


@dataclasses.dataclass
class DriverSchedule:
    driver_phone: str
    start: dt.datetime
    end: dt.datetime

    @classmethod
    def from_json(cls, data):
        data['start'] = dt.datetime.fromisoformat(data['start'])
        data['end'] = dt.datetime.fromisoformat(data['end'])
        return cls(**data)

    def to_json(self):
        data = self.__dict__
        data['start'] = data['start'].isoformat()
        data['end'] = data['end'].isoformat()
        return data


@dataclasses.dataclass
class Transport:
    type: str
    amount: int

    def to_json(self):
        return self.__dict__


@dataclasses.dataclass
class Order:
    id: Optional[int]
    user_phone: str
    driver_phone: Optional[str]
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
        data['driver_phone'] = data.get('driver_phone', None)
        data['status'] = data.get('status', "unknown")
        return cls(**data)

    def to_json(self):
        data = self.__dict__
        print(data)
        data['start'] = data['start'].isoformat()
        data['end'] = data['end'].isoformat()
        return data
