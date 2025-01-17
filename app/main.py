import time
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from . import models, schemas, crud, auth
from .database import engine, get_db
from .config import settings
from .redis import redis_client

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    max_retries = 5
    retry_interval = 5

    for attempt in range(max_retries):
        try:
            models.Base.metadata.create_all(bind=engine)
            print("Database tables created successfully")
            redis_client.ping()
            print("Redis connection successful")
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Startup error, retrying in {retry_interval} seconds... ({attempt + 1}/{max_retries})")
                print(f"Error details: {str(e)}")
                time.sleep(retry_interval)
            else:
                print("Startup failed, maximum retry attempts reached")
                raise e

@app.post("/register")
def register(user: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=15))
    new_refresh_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(days=7))
    crud.add_login_history(db, user_id=user.id, user_agent="some_user_agent")
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    # Using timezone-aware datetime
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

@app.post("/refresh")
def refresh_access_token(current_refresh_token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(
            current_refresh_token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": token_data.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.put("/user/update")
def update_user_data(
    user_data: schemas.UserUpdate,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)]
):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    updated_user = crud.update_user(db, db_user, user_data)
    return updated_user

@app.get("/user/history")
def get_user_history(
        db: Annotated[Session, Depends(get_db)],
        token: Annotated[str, Depends(oauth2_scheme)]
):
    """
    Get the current user's login history.
    Validates user authorization through token.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    # Check if token is invalidated
    if redis_client.get(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been invalidated"
        )

    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    history = crud.get_login_history(db, user_id=user.id)
    return {
        "email": user.email,
        "login_history": history
    }

@app.post("/logout")
def logout(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Log out user and mark the access token as invalid.
    """
    try:
        # Decode access token
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    # Store token in Redis with expiration time (matching token expiration)
    expires = payload.get("exp")  # Get token expiration time (UTC timestamp)
    if expires:
        ttl = expires - datetime.now(timezone.utc).timestamp()
        if ttl > 0:  # Ensure expiration time is valid
            redis_client.setex(token, int(ttl), "invalid")  # Set key as Token, value as "invalid"

    return {"message": "Logged out successfully"}
