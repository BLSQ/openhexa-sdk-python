# Generated by ariadne-codegen
# Source: openhexa/graphql/queries.graphql

from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import CreateWorkspaceError


class CreateWorkspace(BaseModel):
    create_workspace: "CreateWorkspaceCreateWorkspace" = Field(alias="createWorkspace")


class CreateWorkspaceCreateWorkspace(BaseModel):
    success: bool
    workspace: Optional["CreateWorkspaceCreateWorkspaceWorkspace"]
    errors: List[CreateWorkspaceError]


class CreateWorkspaceCreateWorkspaceWorkspace(BaseModel):
    slug: str
    name: str
    description: Optional[str]
    countries: List["CreateWorkspaceCreateWorkspaceWorkspaceCountries"]


class CreateWorkspaceCreateWorkspaceWorkspaceCountries(BaseModel):
    code: str
    alpha_3: str = Field(alias="alpha3")
    name: str


CreateWorkspace.model_rebuild()
CreateWorkspaceCreateWorkspace.model_rebuild()
CreateWorkspaceCreateWorkspaceWorkspace.model_rebuild()
