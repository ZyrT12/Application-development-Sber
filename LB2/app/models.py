from datetime import datetime
from uuid import uuid4, UUID as UUID_TYPE
from typing import List, Optional
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import String, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id: Mapped[UUID_TYPE] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    addresses: Mapped[List["Address"]] = relationship("Address", back_populates="user", cascade="all, delete-orphan")

class Address(Base):
    __tablename__ = "addresses"
    id: Mapped[UUID_TYPE] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID_TYPE] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    street: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    state: Mapped[str] = mapped_column(String, nullable=False)
    zip_code: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user: Mapped["User"] = relationship("User", back_populates="addresses")

class Product(Base):
    __tablename__ = "products"
    id: Mapped[UUID_TYPE] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    price_cents: Mapped[int] = mapped_column(Integer, nullable=False)

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[UUID_TYPE] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID_TYPE] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    address_id: Mapped[UUID_TYPE] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=False)
    product_id: Mapped[UUID_TYPE] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
