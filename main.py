from database import engine, Base
from fastapi import FastAPI
from routers import user, post

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)