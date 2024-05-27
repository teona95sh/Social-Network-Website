from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
#import sys
#sys.path.append('../blog')
import JWTtoken,schemas,database,models
from hashing import Hash

router = APIRouter(
                tags = ['Authentication']
)

@router.post('/login')

def login(request:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"Invalid Credentials")
    
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"Invalid Credentials")

    access_token = JWTtoken.create_access_token(data={"user_id": user.id,"sub": user.email})
        
    return {"access_token": access_token, "token_type": "bearer"}