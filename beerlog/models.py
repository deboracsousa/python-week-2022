#from dataclasses import dataclass

from typing import Optional
from sqlmodel import SQLModel, Field #python vem como padrão o sqlite.
from sqlmodel import select
from pydantic import validator #desde o python 2
from statistics import mean #desde o python 2
from datetime import datetime #desde o python 2

#@dataclass #utiliza o padrão decorator, já coloca __init__, inicializador do objeto.
class Beer(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, index=True)
    name: str
    style: str
    flavor: int
    image: int
    cost: int
    rate: int = 0
    date: datetime = Field(default_factory=datetime.now)

    @validator("flavor", "image", "cost")
    def validate_ratings(cls, v, field):
        if v < 1 or v > 10:
            raise RuntimeError(f"{field.name} must be btween 1 and 10")
        return v

    @validator("rate", always=True)
    def calculate_rate(cls,v, values):
        rate = mean(
            [
                values["flavor"], 
                values["image"], 
                values["cost"]
            ])
        return int(rate)

try:
    brewdog = Beer(name="Brewdog", style="NEIPA", flavor=6, image=8, cost=10)
except RuntimeError:
    print("zika de mais")