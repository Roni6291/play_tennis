from typing import Annotated

from pydantic import BaseModel, Field

from .enums import Humidity, Outlook, Temperature, Wind

Version = Annotated[str, Field(pattern=r'^\d+.\d+.\d+$')]


class Weather(BaseModel):
    outlook: Outlook
    temperature: Temperature
    humidity: Humidity
    wind: Wind


class Playability(BaseModel):
    outlook: Outlook
    temperature: Temperature
    humidity: Humidity
    wind: Wind
    can_play: bool
    description: str
