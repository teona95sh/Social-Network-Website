import schemas,models,oauth2,database
from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from repository import follow

router = APIRouter(
        prefix = "/follow",
        tags = ['Follows']
)

get_db = database.get_db

@router.post('/{target_user_id}',status_code=status.HTTP_201_CREATED,response_model=schemas.Follow)
def create_follow( target_user_id: int,follow1:schemas.FollowCreate,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    return follow.c_follow(target_user_id,follow1,db,current_user.id)

@router.delete('/followings/{target_user_id}',status_code=status.HTTP_200_OK)
def unfollow_user(target_user_id,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    user_id = current_user.id
    return follow.unfollow(target_user_id,db,user_id)