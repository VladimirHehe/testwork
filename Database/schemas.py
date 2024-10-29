from pydantic import BaseModel, EmailStr
from fastapi import UploadFile, File


class UserCreate(BaseModel):
    avatar: UploadFile = File(...)
    gender: str
    first_name: str
    last_name: str
    email: EmailStr
