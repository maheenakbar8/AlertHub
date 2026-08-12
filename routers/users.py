from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import UserCreate, UserResponse, UserPreferencesUpdate
from services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id,
    update_user_preferences
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse)
def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(db, user.email)


@router.get("/", response_model=list[UserResponse])
def read_users(
    db: Session = Depends(get_db)
):
    return get_all_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.put("/{user_id}/preferences", response_model=UserResponse)
def update_preferences(
    user_id: int,
    preferences: UserPreferencesUpdate,
    db: Session = Depends(get_db)
):
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return update_user_preferences(
        db,
        user,
        preferences
    )