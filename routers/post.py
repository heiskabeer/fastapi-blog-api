from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from models import PostModel
from schemas.post import PostBase, PostCreate, PostOut, PostUpdate, PostRead
from database import get_db_session

router = APIRouter(prefix='/posts', tags=['Posts'])

@router.post('/', response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db:Session = Depends(get_db_session)):

    new_post = PostModel(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return PostOut.model_validate(new_post)

@router.get('/', response_model=list[PostOut], status_code=status.HTTP_200_OK)
def get_post(db:Session=Depends(get_db_session)):
    all_post = db.query(PostModel).all()

    return all_post