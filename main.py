from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import random
import string

app = FastAPI()

# Temporary in-memory storage
users = {}

# User model
class User(BaseModel):
    last_name: str = Field(min_length=2, max_length=50)
    identification_number: str = Field(regex="^[0-9]{6,10}$")  # Ensure 6-10 digit ID

# Deactivation request model
class DeactivateRequest(BaseModel):
    identification_number: str
    unique_code: str

# Function to generate a unique 6-digit code
def generate_unique_code():
    return ''.join(random.choices(string.digits, k=6))

@app.post("/add_user")
def add_user(user: User):
    user_id = user.identification_number  # Fixing inconsistent attribute name

    if user_id in users:
        raise HTTPException(status_code=400, detail="User already exists")

    unique_code = generate_unique_code()  # Generate a unique code for deactivation
    users[user_id] = {
        "last_name": user.last_name,
        "identification_number": user_id,
        "active": False,  # Default to inactive until activation
        "unique_code": unique_code
    }
    
    return {"message": "User added successfully", "user_id": user_id, "unique_code": unique_code}

@app.post("/activate")
def activate(user: User):
    user_id = user.identification_number

    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    users[user_id]["active"] = True  # Mark user as active

    return {"message": f"User {user.last_name} activated", "status": True, "unique_code": users[user_id]['unique_code']}

@app.post("/deactivate_user")
def deactivate_user(request: DeactivateRequest):
    user_id = request.identification_number

    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/status/{identification_number}")
def get_status(identification_number: str):
    if identification_number not in users:
        raise HTTPException(status_code=404, detail="User not found")

    user = users[identification_number]
    return {"last_name": user["last_name"], "status": "Active" if user["active"] else "Inactive"}
