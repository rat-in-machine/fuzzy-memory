from app.db.database import SessionLocal
from app.db.models import User

db = SessionLocal()

user = User(
    email="test@mail.com",
    password="123456",
    role="buyer"
)

db.add(user)
db.commit()
db.close()

print("Usuario creado correctamente")
