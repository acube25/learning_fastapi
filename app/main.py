from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from . import models
from .routers import post, user, auth, vote
from .config import settings


print(settings.database_name)


# models.Base.metadata.create_all(bind = engine)

app = FastAPI()

origins = ["https://www.google.com", "https://www.youtube.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# my_post = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
# {"title": "title of post 2", "content": "content of post 2", "id": 2}]

# def find_post(id):
#     for p in my_post:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_post):
#         if p["id"] == id:
#             return i 
@app.get("/")
def root():
    return {"message": "hello"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)