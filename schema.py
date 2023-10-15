from pydantic import BaseModel
import datetime


class FinOperationGet(BaseModel):
    symbol: str | None = None
    account_id: str
    activity_type: str | None = None
    created_time: datetime.datetime
    up: str
    description: str | None = None
    symbol: str
    quantity: float | None = None

    class Config:
        orm_mode = True


class InstrumentsGet(BaseModel):
    id: int
    symbol: str


class ActivityLegsGet(BaseModel):
    quantity: float
    activity_id: int
    instrument_id: int
    price: float


class ActivitiesGet(BaseModel):
    id: int
    account_id: str
    description: str
    activity_type: str
    created_time: datetime.datetime


class AccountsGet(BaseModel):
    id: int
    owner_id: int
    account_id: str
    clearing_code: str


class PrincipalsGet(BaseModel):
    id: int
    up: str