from pydantic import BaseModel, EmailStr
from datetime import date

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    date_of_birth: date
    country: str
    favorite_sport: str
    favorite_team: str
