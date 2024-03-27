import schemas,models,oauth2,database
from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from repository import like
from typing import List


router = APIRouter(
        prefix = "/posts/likes",
        tags = ['Likes']
)

get_db = database.get_db

@router.post('/{post_id}/like',status_code=status.HTTP_201_CREATED, response_model=schemas.LikeBase)
def create_like_for_post(post_id: int,like2: schemas.LikeCreate,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
        user_id = current_user.id
        return like.create_post_like(like2,db,post_id,user_id)

@router.post('/comments/{comment_id}/like',status_code=status.HTTP_201_CREATED, response_model=schemas.LikeBase)
def create_like_for_comment(like2: schemas.LikeCreate,post_id:int,comment_id:int,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
        user_id = current_user.id
        return like.create_comment_like(like2,post_id,db,comment_id,user_id)

@router.delete('/{post_id}/like/{id}',status_code=status.HTTP_200_OK)
def delete_post_like(post_id:int,id:int,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
        user_id = current_user.id
        return like.unlike_post(post_id,id,db,user_id)

@router.delete('/comments/{comment_id}/like/{id}',status_code=status.HTTP_200_OK)
def delete_comment_like(comment_id:int,id:int,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
        return like.unlike_comment(comment_id,id,db,current_user.id)



