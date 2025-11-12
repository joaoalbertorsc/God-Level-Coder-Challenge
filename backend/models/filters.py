from pydantic import BaseModel
from typing import List

class Channel(BaseModel):
    id: int
    name: str

class Store(BaseModel):
    id: int
    name: str

class FilterOptionsResponse(BaseModel):
    channels: List[Channel]
    stores: List[Store]
