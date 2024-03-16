from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
#import sys
#sys.path.append('../blog')
import models,schemas,JWTtoken
from hashing import Hash
from routers import login

def get_user_by_email(email: str, db:Session):
    return db.query(models.User).filter(models.User.email == email).first()

def create(request:schemas.User,db:Session):
    new_user=models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = JWTtoken.create_access_token(data={"sub": new_user.email})
    return {"user": new_user, "access_token": access_token}


def show(id:int,db:Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with the id {id} is not available")
    return user

def destroy(id:int,db:Session):
    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found")

    user.delete(synchronize_session=False)
    db.commit()
    return 'user is successfully deleted'