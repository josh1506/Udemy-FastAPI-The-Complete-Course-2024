from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Users
from routers.auth import get_current_user, bcrypt_context

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class ResetPasswordRequest(BaseModel):
    password: str
    new_password: str = Field(min_length=6, max_length=128)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed.")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    del user_model.hashed_password
    return user_model


@router.put("/update/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_password(user: user_dependency, db: db_dependency, reset_pass_request: ResetPasswordRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed.")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if not bcrypt_context.verify(reset_pass_request.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Authentication failed.")

    user_model.hashed_password = bcrypt_context.hash(reset_pass_request.new_password)
    db.add(user_model)
    db.commit()
