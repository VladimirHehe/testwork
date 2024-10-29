from pydantic import BaseModel, EmailStr



class UserCreate(BaseModel):
    gender: str
    first_name: str
    last_name: str
    email: EmailStr
