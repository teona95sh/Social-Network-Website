import schemas,models,oauth2,database
from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from repository import friend
from typing import List


router = APIRouter(
        prefix = "/friend",
        tags = ['Friends']
)

get_db = database.get_db

@router.post("/friend-request/send/{to_user_id}",status_code=status.HTTP_201_CREATED,response_model=schemas.Friend)
def create_friendship_request(to_user_id :int,request: schemas.FriendCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
        user_id = current_user.id 
        return friend.add_friend(to_user_id,request,db,user_id)

@router.post("/friend-request/respond/{request_id}",status_code=status.HTTP_201_CREATED)
def respond_friendship_request(request_id:int,response:str,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
        user_id = current_user.id 
        return friend.respond_to_friendship_request(request_id,response,db,user_id)


@router.delete("/friend-request/{id}",status_code=status.HTTP_200_OK)
def cancel_friend_request(request_id:int,db:Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
        user_id = current_user.id 
        return friend.cancel_request(request_id,db,user_id)

@router.delete("/friend-delete/{id}",status_code=status.HTTP_200_OK)
def delete_user_from_friends(target_user_id:int,id:int,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
        user_id = current_user.id 
        return friend.delete_friend(target_user_id,id,db,user_id)

@router.get("/friends_list")
def get_friends_list(db:Session=Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
        user_id = current_user.id 
        return friend.show_friends_list(db,user_id)

@router.get("friends/{id}")
def get_friends_list_by_user_id(id:int,db:Session = Depends(get_db)):
        return friend.show_friends_by_user_id(id,db)