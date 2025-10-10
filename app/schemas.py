from uuid import UUID
from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    class Config:
        from_attributes = True


class OCRTitleOut(BaseModel):
    id: UUID
    title: str
    class Config:
        from_attributes = True

class OCRData(BaseModel):
    id: UUID
    page: int
    data: str
    class Config:
        from_attributes = True

class OCRItems(BaseModel):
    id: UUID
    created_at: datetime
    ocr_title: OCRTitleOut
    user: UserOut
    ocr_data: List[OCRData]

    class Config:
        from_attributes = True