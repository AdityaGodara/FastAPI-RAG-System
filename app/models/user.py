from app.models.base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, DateTime, func

class User(Base):
    __tablename__ = "users"

    id : Mapped[UUID] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(nullable=False)

    email: Mapped[str] = mapped_column(nullable=False, unique=True)

    password_hash: Mapped[str] = mapped_column(nullable=False)

    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    is_verified: Mapped[bool] = mapped_column(nullable=False, default=False)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), 
                                                 server_default=func.now(), 
                                                 nullable=False)
    
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), 
                                                 server_default=func.now(), 
                                                 nullable=False)