from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix= "/posts",
    tags = ["Posts"]
)

# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_all_posts(db: Session = Depends(get_db), 
                  current_user: int = Depends(oauth2.get_current_user),
                  limit: int = 10, 
                  skip: int = 0,
                  search: Optional[str] = ""):  
    # cursor.execute("""SELECT * FROM posts""")
    # all_post = cursor.fetchall()

    all_post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #if i want filtering the posts like only see current user, and u don't see current_user see in create_user
    #all_post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = [{"Post": post, "vote": votes} for post, votes in results]

    return posts

@router.get("/{id}", response_model = schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db)): 
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id_n),))
    # post = cursor.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post, vote_count = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}

    # posts = [{"Post": post, "vote": votes} for post, votes in post]
    print(post)
    
    return {
        "Post": post,
        "vote": vote_count
    }

@router.post("/", status_code= status.HTTP_201_CREATED, response_model = schemas.Post)
def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db), 
             current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts(title, content) VALUES (%s, %s) RETURNING *""", 
    #                (new_post.title, new_post.content))
    # post_dict = cursor.fetchone()
    # conn.commit()
    
    # title = new_post.title, content = new_post.content, published = new_post.published & **new_post.dict() are same
    # **dict() means unpack dictionary

    print(current_user.email)

    post_dict = models.Post(owner_id = current_user.id, **new_post.dict())
    db.add(post_dict)
    db.commit()
    db.refresh(post_dict)

    return post_dict

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
             current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # del_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail = "Not authorization to perform requested action")

    post_query.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model= schemas.Post)
def updated_post(id: int, post:  schemas.PostCreate, db: Session = Depends(get_db), 
             current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # upd_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_no = post_query.first()
    
    if post_no == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")

    if post_no.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail = "Not authorization to perform requested action")

    post_query.update(post.dict(), synchronize_session = False)

    db.commit()
    
    return post_query.first()