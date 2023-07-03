from datetime import datetime
from typing import Optional
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
    creation_time: str
        

class ListEnvironmentSchema(_BaseSchema):
    exclude_destroyed: bool = Field(default=True)
    name: Optional[str] = Field(default=None)
    status: Optional[list[StatusEnum]] = Field(default=None)


class EnvironmentNameSchema(_BaseSchema):
    name: str