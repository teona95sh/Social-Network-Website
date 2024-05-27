from database import Base
from sqlalchemy import Column, Integer, String,ForeignKey,Boolean,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True,nullable=False)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False)
    password = Column(String,nullable=False)
    followers = Column(Integer, default=0)
    followings = Column(Integer, default=0)
    friends_count = Column(Integer, default=0)
    posts = relationship("Post",back_populates="owner")
    comments = relationship("Comment", back_populates="owner")
    like_owner = relationship("Like", back_populates="owner")
    follower = relationship(
        "Follow", back_populates="target_user", foreign_keys="Follow.follower_id"
    )
    following = relationship(
        "Follow", back_populates="follower", foreign_keys="Follow.target_user_id"
    )
    sent_friend_requests = relationship(
        "Friendship", foreign_keys="[Friendship.from_user_id]", back_populates="from_user"
    )
    received_friend_requests = relationship(
        "Friendship", foreign_keys="[Friendship.to_user_id]", back_populates="to_user"
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )



class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer,primary_key=True,index=True,nullable=False)
    title = Column(String,nullable=False)
    likes = Column(Integer,default=0)
    total_comments = Column(Integer, default=0)
    content = Column(String,nullable=False)
    is_modified = Column(Boolean, default=False)
    published = Column(Boolean, server_default='TRUE',nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User",back_populates="posts")
    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    modified_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    comments = relationship("Comment")
    #likes = relationship("Like", back_populates="post")


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer,primary_key=True,index=True,nullable=False)
    post_id = Column(Integer,ForeignKey("posts.id", ondelete="CASCADE"),nullable=False)
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner = relationship("User",back_populates="comments")
    likes = Column(Integer, default=0)
    is_modified = Column(Boolean, default=False)
    #comment_owner = relationship("Post",back_populates="comments")
    content = Column(String,nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    modified_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    likes_rel = relationship("Like",back_populates="comments")

class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer,primary_key=True,index=True,nullable=False)
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"))
    post_id = Column(Integer,ForeignKey("posts.id", ondelete="CASCADE"))
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    post = relationship("Post")
    owner = relationship("User", back_populates="like_owner")
    comments = relationship("Comment",back_populates="likes_rel")
    #is_liked = Column(Boolean, default=True)
    #amount = Column(Integer,default=1)

class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"))
    target_user_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )

    follower = relationship(
        "User", back_populates="following", foreign_keys=[follower_id], overlaps = "follower"
    )
    target_user = relationship(
        "User", back_populates="follower", foreign_keys=[target_user_id], overlaps = "following"
    )

class Friendship(Base):
    __tablename__ = "friends"

    id=Column(Integer,primary_key=True,index=True)

    from_user_id = Column(Integer,ForeignKey("users.id"))
    to_user_id = Column(Integer,ForeignKey("users.id"))  
    status = Column(String, default="pending")  # "pending", "accepted", "rejected"
    from_user = relationship("User", foreign_keys=[from_user_id], back_populates="sent_friend_requests")
    to_user = relationship("User", foreign_keys=[to_user_id], back_populates="received_friend_requests")






