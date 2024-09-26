from datetime import datetime, timedelta
from http.client import HTTPException
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

#ключик для JWT
SECRET_KEY = "sekretno"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#для хешинга
pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#генерация токенов
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#сам хешинг и верификация
def verify_password(plain_password, hashed_password):
    return pass_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pass_context.hash(password)

#верификация токена
def verify_token(token):
    credentials_exception = HTTPException()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_id