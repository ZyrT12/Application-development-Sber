from app.db import session_factory
from app.models import User, Address

def run():
    rows = [
        ("john_doe","john@example.com","Baker St 221B","London","LDN","NW1","UK"),
        ("jane_smith","jane@example.com","5th Ave 1","New York","NY","10001","USA"),
        ("mike_miller","mike@example.com","Hauptstr 7","Berlin","BE","10115","DE"),
        ("olga_ivanova","olga@example.com","Nevsky 1","Saint-Petersburg","SPB","190000","RU"),
        ("li_wei","li@example.com","Nanjing Rd 10","Shanghai","SH","200000","CN"),
    ]
    with session_factory() as session:
        for u,e,st,ct,stt,zipc,c in rows:
            user = User(username=u, email=e)
            user.addresses.append(Address(
                street=st, city=ct, state=stt, zip_code=zipc, country=c, is_primary=True
            ))
            session.add(user)
        session.commit()

if __name__ == "__main__":
    run()
