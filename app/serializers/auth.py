from pydantic import BaseModel


class RefreshToken(BaseModel):
    refresh_token: str

    class Config:
        orm_mode = True
