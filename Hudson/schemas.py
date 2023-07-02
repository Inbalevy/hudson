from datetime import datetime
from pydantic import BaseModel
from models import StatusEnum


class TemplateSchema(BaseModel):
    id: int
    name: str
    github_url: str
    enabled: bool
    creation_time: datetime

    class Config:
        orm_mode = True
        

class EnvironmentSchema(BaseModel):
    id: int
    name: str
    template_id: int
    status: StatusEnum
    creation_time: datetime

    class Config:
        orm_mode = True