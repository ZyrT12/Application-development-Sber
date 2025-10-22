from app.db import session_factory
from app.models import User, Address, Product, Order

def run():
    created = 0
    with session_factory() as s:
        users = s.query(User).order_by(User.username).limit(5).all()
        products = s.query(Product).order_by(Product.title).limit(5).all()
        if len(users) < 5:
            print("Нужно минимум 5 пользователей (запусти python -m app.seed, если их нет).")
            return
        if len(products) < 5:
            print("Нужно минимум 5 продуктов (запусти python -m app.seed_products).")
            return

        for user, product in zip(users, products):
            addr: Address = user.addresses[0]
            # сделаем сид идемпотентным: не создавать дубль, если уже есть заказ для этой пары
            exists = (
                s.query(Order)
                 .filter(Order.user_id == user.id,
                         Order.address_id == addr.id,
                         Order.product_id == product.id)
                 .first()
            )
            if exists:
                continue
            s.add(Order(user_id=user.id, address_id=addr.id, product_id=product.id, quantity=1))
            created += 1

        s.commit()
    print(f"Добавлено заказов: {created} (идемпотентно, без дублей)")

if __name__ == "__main__":
    run()
