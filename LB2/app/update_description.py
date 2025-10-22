from app.db import session_factory
from app.models import User

def run():
    pairs = {
        "john_doe": "VIP customer from NY",
        "jane_smith": "Frequent buyer",
    }
    updated = 0
    with session_factory() as s:
        users = s.query(User).filter(User.username.in_(pairs.keys())).all()
        for u in users:
            u.description = pairs[u.username]
            updated += 1
        s.commit()
    print(f"Обновлено пользователей (description): {updated}")

if __name__ == "__main__":
    run()
