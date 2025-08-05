from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from models import UserModel
from schemas.user import UserBase, UserCreate, UserOut, UserRead, UserUpdate
from database import get_db_session


router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{user_id}", response_model=UserOut)
def get_single_user(user_id: int, db: Session = Depends(get_db_session)):
    user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= 'User not Found!'
        )

    return UserOut.model_validate(user) 

@router.get("/", response_model=list[UserOut])
def get_all_users(db: Session = Depends(get_db_session)):
    users = db.query(UserModel).all()
    return users

@router.post("/", response_model=UserOut)
def create_users(user: UserCreate, db: Session = Depends(get_db_session)):
    existing_user = db.query(UserModel).filter(
        (UserModel.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail='User already exists'
        )

    new_user = UserModel(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserOut.model_validate(new_user)

@router.delete("/{user_id}")
def delete_users(user_id, db:Session = Depends(get_db_session)):
    user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail='User not found!'
        )
    
    db.delete(user)
    db.commit()

    return {
        "detail": "Book Successfully deleted",
        "message": user
    }

@router.put("/{user_id}")
def update_user(user_id: int, updated_user:UserCreate, db:Session=Depends(get_db_session)):
    existing_user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if not existing_user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail='User not found!'
        )

    for k,v in updated_user.model_dump().items():
        setattr(existing_user, k, v)

    db.commit()
    db.refresh(existing_user)

    return UserOut.model_validate(existing_user)

@router.patch("/{book_id}", response_model=UserOut)
def patch_user(user_id:int, updates: UserUpdate, db:Session=Depends(get_db_session)):
    existing_user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if not existing_user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    update_data = updates.model_dump(exclude_unset=True)

    for k, v in update_data.items():
        setattr(existing_user, k, v)
    
    db.commit()
    db.refresh(existing_user)

    return UserOut.model_validate(existing_user)
