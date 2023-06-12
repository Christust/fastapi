from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies import (
    create_access_token,
    oauth2_schema,
    create_refresh_token,
    decode_access_token,
    get_db,
)
from app.models.user import User
from app.serializers.auth import RefreshToken

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/")
async def auth(
    data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == data.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales erroneas"
        )
    else:
        if not user.verify_password(data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales erroneas"
            )
        return {
            "access_token": create_access_token(user),
            "refresh_token": create_refresh_token(user),
            "token_type": "Bearer",
        }


@auth_router.post("/refresh-token")
async def refresh_token(refresh_token: RefreshToken, db: Session = Depends(get_db)):
    data = decode_access_token(refresh_token.refresh_token)
    if data:
        user = db.query(User).filter(User.id == data["user_id"]).first()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Error auth"
        )
    return {
        "access_token": create_access_token(user),
        "refresh_token": create_refresh_token(user),
        "token_type": "Bearer",
    }
