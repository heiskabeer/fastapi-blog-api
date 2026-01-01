from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from models import UserModel
from schemas.user import UserBase, UserCreate, UserLogin, UserOut, UserRead, UserUpdate
from database import get_db_session, db_dependency
import auth

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
def read_users_me(current_user: UserOut = Depends(auth.get_current_user)):
    return {"id": current_user.id, "email": current_user.email, 'message': 'this is protected route'}

@router.post("/signup", response_model=UserOut)
def register_user(user: UserCreate, db:db_dependency):
    existing_user = db.query(UserModel).filter(
        UserModel.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail="This email already exists"
        )
    
    hashed_password = auth.hash_password(user.password)
    new_user = UserModel(
        **user.model_dump(exclude=['password']),
        password_hash = hashed_password
        )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserOut.model_validate(new_user)

@router.post("/login")
def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db:db_dependency
    ):
    # Find User in DB
    existing_user = db.query(UserModel).filter(
        UserModel.email == form_data.username
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password'
        )
    
    # verify password
    if not auth.verify_password(form_data.password, existing_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password'
        )
    
    access_token = auth.create_access_token(
        data={"sub": existing_user.email}
    )
    
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }

@router.get("/{user_id}", response_model=UserOut)
def get_single_user(
    user_id: int,
    db:db_dependency, 
    current_user: Annotated[UserModel, Depends(auth.get_current_user)]
    ):
    user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail= 'User not Found!'
        )

    return UserOut.model_validate(user) 

# @router.get("/", response_model=list[UserOut])
# def get_all_users(db:db_dependency):
#     users = db.query(UserModel).all()
#     return users

@router.delete("/me")
def delete_users(
    current_user: Annotated[UserRead, Depends(auth.get_current_user)],
    db:db_dependency
    ):

    db.delete(current_user)
    db.commit()

    return {
        "detail": "User Successfully Deleted!",
        "message": {
            "user_name": current_user.user_name,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name
        }
    }

@router.patch("/me", response_model=UserOut)
def patch_user(
    updates: UserUpdate, 
    current_user: Annotated[UserModel, Depends(auth.get_current_user)], 
    db: db_dependency
):
    update_data = updates.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    if "email" in update_data:
        email_exists = db.query(UserModel).filter(
            UserModel.email == update_data["email"],
            UserModel.id != current_user.id
        ).first()
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This email is already registered"
            )

    for key, value in update_data.items():
        setattr(current_user, key, value)
    
    db.commit()
    db.refresh(current_user)

    return current_user

