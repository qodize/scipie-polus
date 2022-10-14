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
        data['start'] = dt.datetime.fromisoformat(data['start'])
        data['end'] = dt.datetime.fromisoformat(data['end'])
        return cls(id=data.pop('id', None), user=user, driver=driver, transport=transport, **data)

    def to_json(self):
        data = self.__dict__
        data['user'] = self.user.__dict__
        data['driver'] = self.driver.__dict__ if self.driver else None
        data['transport'] = self.transport.__dict__
        return data
