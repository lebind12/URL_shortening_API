from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional


class URL(BaseModel):
    shorten_url: str
    original_url: str
    expire_date: datetime | None
    views: int
    
class URLShortenStatus(BaseModel):
    shorten_url:str

class URLCreate(BaseModel):
    url: str
    expire_date: Optional[str] = None
    
    @field_validator("expire_date")
    def format_check(cls, v):
        if v == None:
            return v
        f = "%Y-%m-%d %H:%M:%S"
        res = True
        try:
            res = bool(datetime.strptime(v, "%Y-%m-%d %H:%M:%S"))
        except ValueError:
            res = False
        if not res:
            raise ValueError("포맷 형식이 맞지 않습니다.")
        return v