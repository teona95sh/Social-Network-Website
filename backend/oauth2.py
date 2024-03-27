from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
import JWTtoken,database,models
from JWTtoken import verify_token

get_db = database.get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},)
            
    user = verify_token(token,credentials_exception,db)
    if user is None:
        raise credentials_exception
    
    return user
