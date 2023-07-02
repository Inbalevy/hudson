from datetime import datetime
from pydantic import BaseModel, Field
from hudson.models import StatusEnum, StateEnum

class _BaseSchema(BaseModel):
    class Config:
        orm_mode = True
    

class TemplateSchema(_BaseSchema):
    id: int
    name: str
    url: str
    state: StateEnum
    creation_time: str
        

class ListTemplatesSchema(_BaseSchema):
    only_enabled: bool = Field(default=False)


class TemplatesNameSchema(_BaseSchema):
    name: str
    

class GithubUrlSchema(_BaseSchema):
    url: str


class EnvironmentSchema(_BaseSchema):
    id: int
    name: str
    template_id: int
    status: StatusEnum = StatusEnum.CREATING
    creation_time: datetime