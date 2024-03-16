import schemas,models,oauth2,database
from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from repository import post
from typing import List


router = APIRouter(
        prefix = "/post",
        tags = ['Posts']
)

get_db = database.get_db


@router.get('/{id}',status_code=200,response_model=schemas.ShowPost)
def show_post(id:int,db:Session=Depends(get_db),current_user: schemas.UserPost = Depends(oauth2.get_current_user)):
    return post.show(id,db,current_user) 

@router.post('/',status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(request: schemas.PostCreate, db: Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    user_id = current_user.id
    return post.create(request = request,db=db,user_id=user_id)

@router.get('/',response_model = List[schemas.ShowPost])
def all_posts(db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    return post.get_all(db,current_user)

@router.get('/{user_id}',response_model = List[schemas.ShowPost])
def all_posts_by_user_id(user_id:int, db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    return post.show_all_by_user_id(user_id,db,current_user)


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int,db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post.destroy(id,db,current_user)

@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id:int,request:schemas.Post,db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    return post.update(id,request,db,current_user)
