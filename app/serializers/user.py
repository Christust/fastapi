from pydantic import BaseModel


class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    username: str | None


class UserOut(UserBase):
    id: int

    class Config:
        schema_extra = {
            "example": {
                "id": "User id",
                "username": "The username",
            }
        }
