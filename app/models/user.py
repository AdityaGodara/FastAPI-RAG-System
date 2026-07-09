import uuid

from app.db.base_class import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, DateTime, String, func, Boolean

class User(Base):
    __tablename__ = "users"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True, nullable=False, default=uuid.uuid4)

    username: Mapped[str] = mapped_column(String(225),nullable=False)

    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    password_hash: Mapped[str] = mapped_column(String(225), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), 
                                                 server_default=func.now(), 
                                                 nullable=False)
    
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), 
                                                 server_default=func.now(), 
                                                 nullable=False)
    
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )