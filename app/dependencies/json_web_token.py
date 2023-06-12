import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.user import User

SECRET_KEY = "CODFA2023"
ALGORITHM = "HS256"

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth")

def decode_access_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as err:
        return None

def get_current_user(token:str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    data = decode_access_token(token)
    if data:
        return db.query(User).filter(User.id == data["user_id"]).first()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error auth")

def create_access_token(user, minutes=7):
    data = {
        "user_id":user.id,
        "username":user.username,
        "exp": datetime.utcnow()+timedelta(minutes=minutes),
    }

    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user):
    data = {
        "user_id":user.id,
        "username":user.username,
        "exp": datetime.utcnow()+timedelta(days=7),
    }

    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)