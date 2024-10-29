import io

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from PIL import Image
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.Database.models import User

from src.Database.db import async_session

router_clients = APIRouter(prefix='/api/clients',
                           tags=["Api клиентов"])


async def add_watermark(image: Image.Image) -> Image.Image:
    """Добавление водяного знака(default avatar)"""
    watermark = Image.open("src/router_client/media/2.png")
    image.paste(watermark, (0, 0), watermark)
    return image


@router_clients.post("/create", tags=["Создание user"])
async def create_user(
    avatar: UploadFile = File(...),
    gender: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    db: AsyncSession = Depends(async_session)
):
    """Создание user"""
    # Проверка уникальности почты
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Обработка аватарки
    image_data = await avatar.read()
    image = Image.open(io.BytesIO(image_data))
    watermarked_image = await add_watermark(image)

    # Сохранение аватарки
    avatar_path = f"avatars/{email}.png"
    watermarked_image.save(avatar_path)

    # Создание нового юзера
    new_user = User(
        avatar=avatar_path,
        gender=gender,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )

    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

    return JSONResponse(status_code=201,
                        content={"message": "User  created successfully", "user": new_user.id})
