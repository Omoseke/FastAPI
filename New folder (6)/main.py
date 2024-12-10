from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from models import User
from schemas import UserCreate
from email_utils import send_activation_email
from passlib.context import CryptContext
from datetime import date

app = FastAPI()
Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/signup/")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash("temporary")  # Set real password later
    new_user = User(
        name=user.name,
        email=user.email,
        date_of_birth=user.date_of_birth,
        country=user.country,
        favorite_sport=user.favorite_sport,
        favorite_team=user.favorite_team,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()

    # Await the email sending coroutine
    await send_activation_email(new_user.email, new_user.id)
    return {"message": "Check your email to activate your account"}


@app.get("/activate/{user_id}")
def activate_account(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = True
    db.commit()
    return {"message": "Account activated! You can now set your password."}

from pydantic import BaseModel

class SetPassword(BaseModel):
    password: str

@app.post("/set-password/")
def set_password(user_id: int, password_data: SetPassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=400, detail="Invalid or inactive user")

    user.hashed_password = pwd_context.hash(password_data.password)
    db.commit()
    return {"message": "Password set successfully"}
