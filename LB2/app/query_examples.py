from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db import session_factory
from app.models import User

def main():
    with session_factory() as session:
        stmt = select(User).options(selectinload(User.addresses))
        for u in session.scalars(stmt):
            print(u.username, "->", [a.street for a in u.addresses])

if __name__ == "__main__":
    main()
