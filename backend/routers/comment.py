import schemas,models,oauth2,database
from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from repository import comment
from typing import List


router = APIRouter(
        prefix = "/posts/comment",
        tags = ['Comments']
)

get_db = database.get_db


@router.post('/{post_id}',status_code=status.HTTP_201_CREATED, response_model=schemas.Comment)
def create_comment(post_id: int,request: schemas.CommentCreate,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    user_id = current_user.id
    return comment.create(request=request,db=db,post_id=post_id,user_id=user_id)

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_comment(id:int,request:schemas.Comment,db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    return comment.update(id,request,db,current_user)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(post_id:int,id:int,db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    comment.destroy(post_id,id,db,current_user)
