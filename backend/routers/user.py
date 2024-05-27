from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,status,HTTPException
import schemas,database,oauth2
from repository import user

router = APIRouter(
        prefix = "/user",
        tags = ['Users']

)

get_db = database.get_db



@router.post('/')
def create_user(request: schemas.User,db:Session=Depends(get_db)):
    db_user = user.get_user_by_email(request.email, db)
    if db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Email already in use")
    return user.create(request,db)


@router.get('/me',response_model = schemas.ShowUser)
async def get_me(current_user: schemas.User = Depends(oauth2.get_current_user)):
    return current_user

@router.get('/{id}',response_model=schemas.ShowUserPosts)
async def get_user(id:int,db:Session=Depends(get_db)):
    return user.show(id,db)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy_user(id:int,db:Session=Depends(get_db)):
    return user.destroy(id,db)