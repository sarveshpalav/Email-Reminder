from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import jwt
import datetime
from fastapi.middleware.cors import CORSMiddleware


from migrations import models  # Import your SQLAlchemy models from your migrations or models file

SECRET_KEY = "email-reminder"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes

# Create the FastAPI app
app = FastAPI()
DATABASE_URL = "postgresql://admin:admin@database/email_reminder_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


origins = [
    "http://localhost:3000",  # Update with your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserSignup(BaseModel):
    email: str
    password: str

def create_access_token(data: dict, expires_delta: datetime.timedelta):
  to_encode = data.copy()
  expire = datetime.datetime.utcnow() + expires_delta
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

  

# Hash a password
def hash_password(password: str):
    return bcrypt.hash(password)

# Dependency to get the database session
def get_db():
  
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Signup route
@app.post("/signup")
async def signup(user_signup: UserSignup, db: Session = Depends(get_db)):
    # Check if the user already exists
    user = db.query(models.User).filter(models.User.email == user_signup.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password before saving to the database
    hashed_password = hash_password(user_signup.password)
    new_user = models.User(email=user_signup.email, password=hashed_password)  # Assuming the column name is 'password'
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Signup successful"}

# Login route
@app.post("/login")
async def login(user_signup: UserSignup, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_signup.email).first()

    if not user or not bcrypt.verify(user_signup.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate a JWT token
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# Health check route
@app.get("/")
async def main_route():
    return {"message": "Server is Healthy"}
