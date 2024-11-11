from pydantic import BaseModel

class Sort(BaseModel):
    field: str = "created_at" 
    direction: str = "asc"

    class Config:
        orm_mode = True