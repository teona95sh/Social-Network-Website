from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Depends
import models,schemas


def create_post_like(like: schemas.LikeCreate,db:Session,post_id:int,user_id:int):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        existing_like = db.query(models.Like).filter(models.Like.post_id == post.id, models.Like.owner_id == user_id).first()
        if not existing_like:
            new_like =  models.Like(owner_id=user_id,post_id=post_id)
            db.add(new_like)
            db.commit()
            db.refresh(new_like)
            count = (
                db.query(models.Like).filter(models.Like.post_id == post_id).count() )
            (
             db.query(models.Post).filter(models.Post.id == post_id).update({models.Post.likes: count})
            )
            db.commit()
            return new_like
        else:
            return existing_like
    else:
        raise HTTPException(status_code=404, detail="Post not found")

    
    

def create_comment_like(like: schemas.LikeCreate,post_id:int,db:Session,comment_id:int,user_id:int):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if comment:
        existing_like = db.query(models.Like).filter(models.Like.comment_id == comment.id, models.Like.owner_id == user_id).first()
        if not existing_like:
            new_like =  models.Like(owner_id=user_id,post_id=post_id,comment_id=comment_id)
            db.add(new_like)
            db.commit()
            db.refresh(new_like)
            count = (
            db.query(models.Like).filter(models.Like.comment_id == comment_id).count() )
            (
            db.query(models.Comment).filter(models.Comment.id == comment_id).update({models.Comment.likes: count})
            )
            db.commit()
            return new_like
        else:
            return existing_like
    else:
        raise HTTPException(status_code=404, detail="Comment not found")
    


    
def unlike_comment(comment_id:int,id:int,db:Session,user_id:int):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if comment:
        existing_like = db.query(models.Like).filter(models.Like.comment_id == comment_id, models.Like.owner_id == user_id).first()
        if existing_like:
           like = db.query(models.Like).filter_by(owner_id=user_id).filter(models.Like.id == id)
           if not like.first():
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Like with id {id} not found")
           like.delete(synchronize_session=False)
           db.commit()
           count = (db.query(models.Like).filter(models.Like.comment_id == comment_id).count())
           ( db.query(models.Comment).filter(models.Comment.id == comment_id).update({models.Comment.likes: count}, synchronize_session=False)
           )
           db.commit()
           return "comment is successfully unliked"
        


def unlike_post(post_id: int,id:int,db:Session,user_id:int): 
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        existing_like = db.query(models.Like).filter(models.Like.post_id == post.id, models.Like.owner_id == user_id).first()
        if existing_like:
           like = db.query(models.Like).filter_by(owner_id=user_id).filter(models.Like.id == id)
           if not like.first():
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Like with id {id} not found")
           like.delete(synchronize_session=False)
           db.commit()
           count = (
            db.query(models.Like)
            .filter(models.Like.post_id == post_id)
            .count()
           )
           (
            db.query(models.Post)
            .filter(models.Post.id == post_id)
            .update({models.Post.likes: count})
           )
           db.commit()
           return "post is successfully unliked"




