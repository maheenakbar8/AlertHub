from sqlalchemy.orm import Session

from models import User


def create_user(db: Session, email: str):
    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        return existing_user

    user = User(email=email)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def update_user_preferences(
    db: Session,
    user: User,
    preferences
):
    user.wants_weather = preferences.wants_weather
    user.wants_news = preferences.wants_news

    db.commit()
    db.refresh(user)

    return user

def user_wants_alert(user, alert_type: str) -> bool:
    if alert_type == "weather":
        return user.wants_weather

    if alert_type in {
        "earthquake",
        "flood",
        "wildfire",
        "cyberattack"
    }:
        return user.wants_news

    return False