from pydantic import BaseModel


class PingBase(BaseModel):
    id: int
    ping_counter: int

    class Config:
        orm_mode = True
