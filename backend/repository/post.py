from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Depends
import models,schemas,oauth2
from routers import user
from sqlalchemy import func

def show(id:int,db:Session, user: schemas.UserPost):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with the id {id} is not available")

    return post

def create(request:schemas.PostCreate,db:Session,user_id:int):
    new_post = models.Post(owner_id=user_id,title=request.title,content=request.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

def get_all(db:Session,user: int):
    posts = db.query(models.Post).filter(models.Post.owner_id == user.id).all()
    return posts

def show_all_by_user_id(id:int, db:Session,current_user: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_posts = db.query(models.Post).filter(models.Post.user_id == id).all()

    return user_posts

def destroy(id:int,db:Session,user:int):
    post = db.query(models.Post).filter_by(owner_id=user.id).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")

    post.delete(synchronize_session=False)
    db.commit()
    return 'post is successfully deleted'

def update(id:int,request: schemas.Post,db:Session,user:int):
    post = db.query(models.Post).filter_by(owner_id=user.id).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} not found")

    post.update({'title': request.title, 'content': request.content})
    post.update({'is_modified': True, 'modified_at': func.now()})
    db.commit()
    return 'updated successfully'

