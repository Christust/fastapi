from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy.orm import Session
from app.models.user import User
from app.serializers.user import UserOut, UserCreate, UserUpdate
from app.dependencies.database import get_db
from app.dependencies.json_web_token import oauth2_schema

user_router = APIRouter(
    prefix="/users", tags=["users"], dependencies=[Depends(oauth2_schema)]
)


async def set_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()


@user_router.get("/", response_model=list[UserOut])
async def index(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@user_router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create(user_params: UserCreate, db: Session = Depends(get_db)):
    user_dict = user_params.dict()
    user = User(**user_dict)
    user.set_password(user_dict["password"])
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@user_router.get("/{user_id}", response_model=UserOut)
async def show(user: Annotated[User, Depends(set_user)]):
    return user


@user_router.put("/{user_id}", response_model=UserOut)
async def update(
    user_params: UserUpdate,
    user: Annotated[User, Depends(set_user)],
    db: Session = Depends(get_db),
):
    if user_params.username:
        user.username = user_params.username
        db.commit()
        db.refresh(user)
    return user


@user_router.delete("/{user_id}")
async def delete(
    user: Annotated[User, Depends(set_user)], db: Session = Depends(get_db)
):
    print(user)
    if user:
        delet = db.delete(user)
        db.commit()
        print(delet)
        return {"message": "Deleted"}
    return {"message": "No existe el usuario"}
