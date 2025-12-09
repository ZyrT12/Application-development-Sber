from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Integer,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


# Тип UUID, чтобы удобно использовать в аннотациях
UUID_TYPE = UUID


class Base(DeclarativeBase):
    """Базовый класс для всех ORM-моделей."""
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID_TYPE] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    username: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )
    email: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )
    # Это поле есть в модели, но в БД его добавит отдельная миграция
    description: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # Связь: один пользователь -> много адресов
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # Связь: один пользователь -> много заказов
    orders: Mapped[List["Order"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[UUID_TYPE] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    user_id: Mapped[UUID_TYPE] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    city: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    street: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    zip_code: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    country: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    # Обратная связь к пользователю
    user: Mapped["User"] = relationship(
        back_populates="addresses",
    )

    # Один адрес может фигурировать в нескольких заказах
    orders: Mapped[List["Order"]] = relationship(
        back_populates="address",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, city={self.city!r})"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[UUID_TYPE] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    title: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )
    # цена в центах, чтобы не возиться с float
    price_cents: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # Один продукт может быть во множестве заказов
    orders: Mapped[List["Order"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, title={self.title!r})"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[UUID_TYPE] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    user_id: Mapped[UUID_TYPE] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    address_id: Mapped[UUID_TYPE] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("addresses.id"),
        nullable=False,
    )
    product_id: Mapped[UUID_TYPE] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("products.id"),
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    # Связи для удобной навигации:
    # o.user.username, o.address.city, o.product.title и т.п.
    user: Mapped["User"] = relationship(
        back_populates="orders",
    )
    address: Mapped["Address"] = relationship(
        back_populates="orders",
    )
    product: Mapped["Product"] = relationship(
        back_populates="orders",
    )

    def __repr__(self) -> str:
        return (
            f"Order(id={self.id!r}, user_id={self.user_id!r}, "
            f"product_id={self.product_id!r}, quantity={self.quantity!r})"
        )
