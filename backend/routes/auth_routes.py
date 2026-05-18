from fastapi import APIRouter
from fastapi import Depends

from pydantic import BaseModel

from sqlalchemy.orm import Session

from database import SessionLocal

from models import User

from passlib.context import CryptContext

from auth import create_access_token

router = APIRouter()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


class RegisterRequest(BaseModel):
    email: str
    password: str



def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(
    req: RegisterRequest,
    db: Session = Depends(get_db),
):

    hashed_password = pwd_context.hash(req.password)

    user = User(
        email=req.email,
        password=hashed_password,
    )

    db.add(user)

    db.commit()

    token = create_access_token(
        {"sub": req.email}
    )

    return {
        "token": token
    }
