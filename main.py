from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select

app = FastAPI()

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    password: str

engine = create_engine("sqlite:///database.db")

def create_db_and_users():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        users = [
            User(username="Santos", password="uide.2026"),
            User(username="James", password="ciberseguridad"),
            User(username="Hollow", password="Knight")
        ]

        for user in users:
            existing = session.exec(
                select(User).where(User.username == user.username)
            ).first()

            if not existing:
                session.add(user)

        session.commit()
@app.on_event("startup")
def on_startup():
    create_db_and_users()
@app.post("/login")
def login(user: User):
    with Session(engine) as session:
        db_user = session.exec(
            select(User).where(User.username == user.username)
        ).first()

        if db_user and db_user.password == user.password:
            return {"message": "Login exitoso"}

    raise HTTPException(status_code=401, detail="Usuario o Contraseña incorrectos")
