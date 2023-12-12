from pydantic import BaseModel, Field
import datetime


class Measurement(BaseModel):
    value: float
    clothes: bool
    date: datetime.datetime = Field(default_factory=datetime.datetime.now)
