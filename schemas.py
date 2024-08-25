# schemas.py
from pydantic import BaseModel
from typing import List

class CategoryKeywordsModel(BaseModel):
    food: List[str]
    computer: List[str]
    electronic: List[str]
    stationery: List[str]
    hotels: List[str]

class SentimentModel(BaseModel):
    text: str