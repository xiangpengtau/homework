from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional

# Base Schemas
class ApiV1GroupCreateSchema(BaseModel):
    id: UUID
    name: str
    number: str

class ApiV1GroupGetSchema(BaseModel):
    id: UUID
    name: str
    number: str

class ApiV1StudentCreateSchema(BaseModel):
    id: UUID
    name: str
    number: str

class ApiV1StudentGetSchema(BaseModel):
    id: UUID
    name: str
    number: str
    group_id: Optional[UUID] = None  # Student may belong to a group

# List Response Schemas
class ApiV1GroupListSchema(BaseModel):
    groups: List[ApiV1GroupGetSchema]

class ApiV1StudentListSchema(BaseModel):
    students: List[ApiV1StudentGetSchema]

# Delete Operation Response Schemas
class ApiV1StudentDeleteResponseSchema(BaseModel):
    success: bool
    message: str
    student_id: UUID

class ApiV1GroupDeleteResponseSchema(BaseModel):
    success: bool
    message: str
    group_id: UUID

# Group Student Operation Schemas
class ApiV1StudentGroupAssignSchema(BaseModel):
    student_id: UUID
    group_id: UUID

class ApiV1StudentGroupRemoveSchema(BaseModel):
    student_id: UUID
    group_id: UUID

class ApiV1StudentGroupTransferSchema(BaseModel):
    student_id: UUID
    from_group_id: UUID
    to_group_id: UUID

# Group Students List Response Schema
class ApiV1GroupStudentsSchema(BaseModel):
    group_id: UUID
    group_name: str
    students: List[ApiV1StudentGetSchema]
