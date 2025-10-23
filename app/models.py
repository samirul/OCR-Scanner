import uuid
from typing import List
from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .database import Base

class User(Base):
    __tablename__ = 'user'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    ocr_title: Mapped[List["OCRTitle"]] = relationship(back_populates="user")


class OCRTitle(Base):
    __tablename__ = "ocr_title"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text('now()'))
    ocr_data: Mapped[List["OCRData"]] = relationship(back_populates="ocr_title", order_by="OCRData.page")
    user: Mapped["User"] = relationship(back_populates="ocr_title")

class OCRData(Base):
    __tablename__ = "ocr_data"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ocr_title.id", ondelete="CASCADE"), nullable=False)
    page: Mapped[int] = mapped_column(Integer, nullable=False)
    data: Mapped[str] = mapped_column(String, nullable=False)
    ocr_title: Mapped["OCRTitle"] = relationship(back_populates="ocr_data")