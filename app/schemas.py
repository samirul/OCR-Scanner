from uuid import UUID
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

class UserOutResponse(BaseModel):
    id: UUID
    email: EmailStr
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    id: UUID
    email: EmailStr
    class Config:
        from_attributes = True

class GetPath(BaseModel):
    path: str
    class Config:
        from_attributes = True


class CeleryOutResponse(BaseModel):
    task_id: UUID
    class Config:
        from_attributes = True


class OCRTitleCreated(BaseModel):
    title: str
    user_id: UUID
    class Config:
        from_attributes = True

class OCRDataCreated(BaseModel):
    title_id: UUID
    page: int
    data: str
    class Config:
        from_attributes = True


class OCRTitlesOut(BaseModel):
    id: UUID
    title: str
    user_id: UUID
    class Config:
        from_attributes = True

class OCRDataOut(BaseModel):
    id: UUID
    page: int
    data: str
    class Config:
        from_attributes = True

class OCRDataDetailedOut(BaseModel):
    id: UUID
    title: str
    user: UserOutResponse
    created_at: datetime
    ocr_data: List[OCRDataOut]

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    id: Optional[str] = None