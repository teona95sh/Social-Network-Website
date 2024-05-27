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
    
def show_followers_list(db:Session,user_id:int):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    followers = (
    db.query(models.Follow.follower_id,models.User.name)
    .join(models.User,models.Follow.follower_id == models.User.id)
    .filter(models.Follow.target_user_id == user_id)
    .all()
)
    followers_list = [{"follower_id": follower.follower_id,"follower_name": follower.name} for follower in followers]
    if (followers):
        return followers_list  
    else:
        return "followers list is empty"

def show_followings_list(db:Session,user_id:int):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    followings = (
    db.query(models.Follow.target_user_id,models.User.name)
    .join(models.User,models.Follow.target_user_id == models.User.id)
    .filter(models.Follow.follower_id == user_id)
    .all()
)
    
    followings_list = [{"following_id": follower.target_user_id,"following_name": follower.name} for follower in followings]
    if (followings):
        return followings_list  
    else:
        return "followings list is empty" 

         
 
        

        