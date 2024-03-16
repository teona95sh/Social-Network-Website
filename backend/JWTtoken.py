from datetime import datetime, timedelta
from jose import JWTError, jwt
import schemas,database,models
from sqlalchemy.orm import Session
from repository import user
from fastapi import Depends


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

get_db = database.get_db


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        #if email is None:
        #    raise credentials_exception

        id: str = payload.get("user_id")
        if id is None or email is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    #curr_user = user.get_user_by_email(email,db)
    #if curr_user is None:
    #       raise credentials_exception
    return token_data