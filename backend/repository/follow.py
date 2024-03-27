from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Depends
import models,schemas


def c_follow(target_user_id: int,follow:schemas.FollowCreate,db:Session,user_id:int):
    target_user = db.query(models.User).filter(models.User.id == target_user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Target user not found")
    db_follow = db.query(models.Follow).filter(models.Follow.follower_id == user_id, 
        models.Follow.target_user_id == target_user_id).first()
    if not db_follow:
        follow_user = models.Follow(follower_id=user_id,target_user_id=target_user_id)
        db.add(follow_user)
        db.commit()
        db.refresh(follow_user)

        count_user_followers = (
            db.query(models.Follow).filter(models.Follow.target_user_id == target_user_id).count()
        )

        (
            db.query(models.User).filter(models.User.id == target_user_id)
            .update({models.User.followers: count_user_followers})
        )

        count_user_followings = (
            db.query(models.Follow).filter(models.Follow.follower_id == user_id).count()
        )

        (
            db.query(models.User).filter(models.User.id == user_id)
            .update({models.User.followings: count_user_followings})
        ) 
        db.commit()
        return follow_user
    else:
        return db_follow
    
def unfollow(target_user_id:int,db:Session,user_id:int):
    target_user = db.query(models.User).filter(models.User.id == target_user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Target user not found")
    db_follow = db.query(models.Follow).filter(
        models.Follow.follower_id == user_id,  
        models.Follow.target_user_id == target_user_id
    ).first()
    if db_follow:
        db.delete(db_follow)
        db.commit()
        count_user_followers = (
            db.query(models.Follow).filter(models.Follow.target_user_id == target_user_id).count()
        )

        (
            db.query(models.User).filter(models.User.id == target_user_id)
            .update({models.User.followers: count_user_followers})
        )

        count_user_followings = (
            db.query(models.Follow).filter(models.Follow.follower_id == user_id).count()
        )

        (
            db.query(models.User).filter(models.User.id == user_id)
            .update({models.User.followings: count_user_followings})
        ) 
        db.commit()
        return "successfully unfollowed"
    else:
        raise HTTPException(status_code=400, detail="User is not being followed")