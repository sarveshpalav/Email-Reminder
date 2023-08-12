from fastapi import FastAPI  
from pydantic import BaseModel


app = FastAPI()  


class UserSignup(BaseModel):
    email: str
    password: str



@app.get("/") 
async def main_route():     
  return {"message": "Server is Healthy"}


@app.post("/signup")
async def signup(user_signup: UserSignup):
    # Here you can implement the signup logic, such as creating a new user in a database
    # You can access user_signup.username, user_signup.email, and user_signup.password
    
    # For now, let's return a simple message indicating successful signup
    return {"message": "Signup successful"}