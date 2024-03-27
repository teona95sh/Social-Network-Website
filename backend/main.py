from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routers import post,user,login,comment,like,follow,friend


app= FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind = engine)
@app.get("/")
async def root():
    return {"message": "Welcome to Reachy"}

app.include_router(login.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(like.router)
app.include_router(follow.router)
app.include_router(friend.router)