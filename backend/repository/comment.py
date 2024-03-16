from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Depends
import models,schemas
from sqlalchemy import func


def create(request: schemas.CommentCreate,db:Session,post_id:int,user_id:int):

    new_comment =  models.Comment(owner_id=user_id,content=request.content,post_id=post_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    count = (
            db.query(models.Comment)
            .filter(models.Comment.post_id == post_id)
            .count()
        )
    (
        db.query(models.Post)
        .filter(models.Post.id == post_id)
        .update({models.Post.total_comments: count})
    )
    db.commit()
    return new_comment

def update(id:int,request:schemas.Comment,db:Session,user:int):

    comment = db.query(models.Comment).filter_by(owner_id=user.id).filter(models.Comment.id == id)

    if not comment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Comment with id {id} not found")

    comment.update({'content': request.content})
    comment.update({'is_modified': True, 'modified_at': func.now()})
    db.commit()
    #db.refresh(comment)
    return 'comment is successfully updated'

def destroy(post_id:int,id:int,db:Session,user:int):
    comment = db.query(models.Comment).filter_by(owner_id=user.id).filter(models.Comment.id == id)
    if not comment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Comment with id {id} not found")

    comment.delete(synchronize_session=False)
    db.commit()
    count = (
            db.query(models.Comment)
            .filter(models.Comment.post_id == post_id)
            .count()
        )
    (
        db.query(models.Post)
        .filter(models.Post.id == post_id)
        .update({models.Post.total_comments: count})
    )
    db.commit()
    return 'comment is successfully deleted'