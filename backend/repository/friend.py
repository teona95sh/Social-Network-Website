from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Depends
import models,schemas


def add_friend(to_user_id: int,request: schemas.FriendCreate,db:Session,user_id: int):
    to_user = db.query(models.User).filter(models.User.id == to_user_id).first()
    if not to_user:
        raise HTTPException(status_code=404, detail="User not found")
    # Check if there is a friend request between the two users with status "accepted"
    accepted_request = (db.query(models.Friendship).filter(
            (
                (models.Friendship.from_user_id == user_id)
                & (models.Friendship.to_user_id == to_user_id)
            )
            |(
                (models.Friendship.from_user_id == to_user_id)
                & (models.Friendship.to_user_id == user_id)
            ), models.Friendship.status == "accepted").first())
    # Check if there is a pending friend request
    existing_request = (db.query(models.Friendship).filter(
            (
                (models.Friendship.from_user_id == user_id)
                & (models.Friendship.to_user_id == to_user_id)
            )
            |(
                (models.Friendship.from_user_id == to_user_id)
                & (models.Friendship.to_user_id == user_id)
            ), models.Friendship.status == "pending").first())
    
    if existing_request:
        raise HTTPException(status_code=400, detail="Friend request already sent")

    if not accepted_request:
            friend_request = models.Friendship(from_user_id=user_id, to_user_id=to_user_id, status="pending")
            db.add(friend_request)
            db.commit()
            db.refresh(friend_request)
            return friend_request
    else:        
        raise HTTPException(status_code=400, detail="Users are already friends")
    
def respond_to_friendship_request(request_id:int,response:str,db:Session,user_id: int):
    friend_request = db.query(models.Friendship).filter(models.Friendship.id == request_id).first()
    if not friend_request:
        raise HTTPException(status_code=404, detail="Friend request not found")
    if friend_request.to_user_id != user_id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to respond to this request"
        )
    accepted_request = (db.query(models.Friendship).filter(
            (
                (models.Friendship.from_user_id == friend_request.from_user_id)
                & (models.Friendship.to_user_id == friend_request.to_user_id)
            )
            |(
                (models.Friendship.from_user_id == friend_request.to_user_id)
                & (models.Friendship.to_user_id == friend_request.from_user_id)
            ), models.Friendship.status == "accepted").first())
    if accepted_request:
        raise HTTPException(status_code=400, detail="Users are already friends")
    
    if response.lower() == "accept":
        friend_request.status = "accepted"
        user1 = db.query(models.User).filter(models.User.id == friend_request.from_user_id).first()
        user2 = db.query(models.User).filter(models.User.id == friend_request.to_user_id).first()

        if user1 and user2:
            user1.friends_count += 1
            user2.friends_count += 1

        db.commit()


    elif response.lower() == "reject":
        friend_request.status = "rejected"
    else:
        raise HTTPException(status_code=400, detail="Invalid response")
    db.commit()

    return {"message": f"Friend request {response}ed successfully"}

def delete_friend(target_user_id:int,id:int,db:Session,user_id:int):
    friend = db.query(models.Friendship).filter(models.Friendship.id == id).first()
    target_user = db.query(models.User).filter(models.User.id == target_user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not friend:
        raise HTTPException(status_code=404, detail="Friend request not found")
    else:
        accepted_friend = (db.query(models.Friendship).filter(
            (
                (models.Friendship.from_user_id == user_id)
                & (models.Friendship.to_user_id == target_user_id)
            )
            |(
                (models.Friendship.from_user_id == target_user_id)
                & (models.Friendship.to_user_id == user_id)
            ), models.Friendship.status == "accepted"))
        if accepted_friend.first():
            accepted_friend.delete(synchronize_session=False)
            db.commit()
            count_user_friends1 = db.query(models.Friendship).filter(models.Friendship.from_user_id == user_id).count()
            count_user_friends2 = db.query(models.Friendship).filter(models.Friendship.from_user_id == target_user_id).count()
            db.query(models.User).filter(models.User.id == user_id).update({models.User.friends_count: count_user_friends1})
            db.query(models.User).filter(models.User.id == target_user_id).update({models.User.friends_count: count_user_friends2})

            db.commit()
            
            return "user successfully deleted from friends"
        

def cancel_request(request_id:int,db:Session,user_id:int):
    friend_request = db.query(models.Friendship).filter(models.Friendship.id == request_id).first()
    if not friend_request:
        raise HTTPException(status_code=404, detail="Friend request not found")
    
    if friend_request.from_user_id != user_id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to cancel this friend request"
        )
    if friend_request.status == "accepted":
        raise HTTPException(
            status_code=400, detail="Cannot cancel an already accepted friend request"
        )
    if friend_request.status == "pending":
       db.delete(friend_request)
       db.commit()
       return "friend request successfully canceled"
 
def show_friends_list(db:Session,user_id:int):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    friends = (
                    db.query(models.User)
                   .join(models.Friendship, models.User.id != user_id)
                   .filter(
                   ((models.Friendship.from_user_id == user_id) | 
                   (models.Friendship.to_user_id == user_id)) &
                   ((models.Friendship.from_user_id == models.User.id) |
                   (models.Friendship.to_user_id == models.User.id)),
                    models.Friendship.status == "accepted").all()
                )

    friends_list = [{"id": friend.id, "name": friend.name} for friend in friends]

    return friends_list

def show_friends_by_user_id(id:int,db:Session):
        user = db.query(models.User).filter(models.User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        friends = (
                    db.query(models.User)
                   .join(models.Friendship, models.User.id != id)
                   .filter(
                   ((models.Friendship.from_user_id == id) | 
                   (models.Friendship.to_user_id == id)) &
                   ((models.Friendship.from_user_id == models.User.id) |
                   (models.Friendship.to_user_id == models.User.id)),
                    models.Friendship.status == "accepted").all()
                )
        friends_list = [{"id": friend.id, "name": friend.name} for friend in friends]

        return friends_list










