from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ObservableFeatures(BaseModel):
    species: Optional[str]
    breed: Optional[str]
    size: Optional[str]
    coat_length: Optional[str]
    coat_color: Optional[str]

class AnimalSaleEntry(BaseModel):
    id: int
    date: datetime
    species: str
    breed: str
    size: str
    weight: float
    coat_length: str
    coat_color: str
    price: float
    client_name: str
    client_email: str