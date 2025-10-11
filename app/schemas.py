from uuid import UUID
from datetime import datetime
from typing import List
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
    id: UUID
    class Config:
        from_attributes = True


class OCRTitleOut(BaseModel):
    id: UUID
    title: str
    class Config:
        from_attributes = True

class OCRDataOut(BaseModel):
    id: UUID
    page: int
    data: str
    class Config:
        from_attributes = True

class OCRItemsOut(BaseModel):
    id: UUID
    created_at: datetime
    ocr_title: OCRTitleOut
    user: UserOutResponse
    ocr_data: List[OCRDataOut]

    class Config:
        from_attributes = True