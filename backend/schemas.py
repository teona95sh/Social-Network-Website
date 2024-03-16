from pydantic import BaseModel, Field, EmailStr
from typing import List,Optional
from datetime import datetime

class FriendBase(BaseModel):
    from_user_id: int
    to_user_id: int
    status: str

class FriendCreate(FriendBase):
    pass

class Friend(FriendBase):
    id: int

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class ShowUser(BaseModel):

    id:int
    name:str
    email:str
    followings:int
    followers:int
    friends_count: int
    #friends_list: List[Friend]=[]

    #created_at: datetime
    

    class Config():
        orm_mode = True

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id:int
    created_at: datetime
    owner_id: int
    post_id: int
    likes: int
    modified_at: datetime
    is_modified: bool
    owner: ShowUser

    class Config():
        orm_mode=True

class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    modified_at: datetime
    is_modified: bool
    owner: ShowUser    
    class Config():
        orm_mode = True

class ShowUserPosts(ShowUser):
    posts: List[Post]=[]

    class Config():
        orm_mode = True



class ShowPost(PostBase):
    id: int
    owner_id: int
    owner: ShowUser
    likes: int
    total_comments: int
    comments: List[Comment]=[]

    class Config:
        orm_mode = True

class User(BaseModel):
    name: str
    email:str
    password:str
    followers: Optional[int]
    followings: Optional[int]
    friends_count: Optional[int]
    created_at: Optional[datetime]
    #friends_list: List[Friend]=[]



    class Config():
        orm_mode=True

class UserPost(User):
    id: int 

    class Config():
        orm_mode=True

class LikeBase(BaseModel):
    id: int
    post_id: Optional[int]
    comment_id : Optional[int]
    owner_id: int
    post: Optional[ShowPost] = None
    owner: ShowUser

    class Config:
        orm_mode = True

class LikeCreate(BaseModel):
    pass


class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    email: Optional[str] = None




class FollowBase(BaseModel):
    follower_id: int
    target_user_id: int

class FollowCreate(FollowBase):
    pass

class Follow(FollowBase):
    id: int
    follower: ShowUser
    target_user: ShowUser

    class Config:
        orm_mode = True

