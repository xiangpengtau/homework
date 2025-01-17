from datetime import datetime  # Import datetime module
from sqlalchemy.orm import Session
from . import models
from . import schemas
from .auth import get_password_hash  # Import get_password_hash function

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: models.User, user_data: schemas.UserUpdate):
    if user_data.email:
        user.email = user_data.email
    if user_data.password:
        user.password_hash = get_password_hash(user_data.password)
    db.commit()
    db.refresh(user)
    return user

def add_login_history(db: Session, user_id: int, user_agent: str):
    db_history = models.LoginHistory(user_id=user_id, user_agent=user_agent, login_time=datetime.utcnow())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

from sqlalchemy.orm import Session
from .models import LoginHistory

# Get login history
# Get login history including user email
def get_login_history(db: Session, user_id: str):
    histories = db.query(LoginHistory).filter(LoginHistory.user_id == user_id).all()
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not histories or not user:
        return []

    return [
        {
            "email": user.email,
            "id": str(history.id),
            "user_agent": history.user_agent,
            "login_time": history.login_time.isoformat()
        }
        for history in histories
    ]
