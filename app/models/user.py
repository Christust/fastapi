from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.username

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)
    
    def set_password(self, password):
        self.password = pwd_context.hash(password)

