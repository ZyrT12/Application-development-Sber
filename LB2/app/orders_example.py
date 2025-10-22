from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.db import session_factory
from app.models import Order

def main():
    with session_factory() as s:
        stmt = select(Order).options(
            joinedload(Order.user),
            joinedload(Order.address),
            joinedload(Order.product),
        )
        for o in s.scalars(stmt):
            print(f"order={o.id} | user={o.user.username} | product={o.product.title} "
                  f"| qty={o.quantity} | ship_to={o.address.city}, {o.address.street}")

if __name__ == "__main__":
    main()
