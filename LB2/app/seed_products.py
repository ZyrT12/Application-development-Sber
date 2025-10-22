from app.db import session_factory
from app.models import Product

def run():
    data = [
        ("Book",     1500),
        ("Pen",       200),
        ("Laptop", 150000),
        ("Backpack", 4500),
        ("Mouse",    2500),
    ]
    added = 0
    with session_factory() as s:
        existing = {p.title for p in s.query(Product.title).all()}
        for title, price in data:
            if title in existing:
                continue
            s.add(Product(title=title, price_cents=price))
            added += 1
        s.commit()
    print(f"Добавлено продуктов: {added} (всего в БД может быть больше, если запускали раньше)")

if __name__ == "__main__":
    run()
