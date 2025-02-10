from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import string

app = FastAPI()

# Temporary in-memory storage
users = {}

# User model
class User(BaseModel):
    last_name: str = Field(min_length=2, max_length=50)
    identification_number: str = Field(regex="^[0-9]{6,10}$")

# Deactivation request model
class DeactivateRequest(BaseModel):
    identification_number: str
    unique_code: str

# Function to generate a unique 6-digit code
def generate_unique_code():
    return ''.join(random.choices(string.digits, k=6))

@app.post("/add_user")
def add_user(user: User):
    # Logic to add user to a database or in-memory store
    users[user.id_number] = {"last_name": user.last_name, "identification_number": user.id_number}
    return {"success": True}
    

@app.post("/activate")
def activate(user: User):
    user_id = user.identification_number

    if user_id not in users:
        unique_code = generate_unique_code()  # Generate unique code for deactivation
        users[user_id] = {"last_name": user.last_name, "active": True, "unique_code": unique_code}
    else:
        users[user_id]["active"] = True

    return {"message": f"User {user.last_name} activated", "status": True, "unique_code": users[user_id]["unique_code"]}

@app.post("/deactivate_user")
def deactivate_user(request: DeactivateRequest):
    user_id = request.identification_number

    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    if users[user_id]["unique_code"] != request.unique_code:
        raise HTTPException(status_code=403, detail="Invalid unique code")

    users[user_id]["active"] = False
    return {"message": f"User {users[user_id]['last_name']} deactivated successfully", "status": False}

@app.get("/status/{identification_number}")
def get_status(identification_number: str):
    if identification_number not in users:
        raise HTTPException(status_code=404, detail="User not found")

    user = users[identification_number]
    return {"last_name": user["last_name"], "status": "Active" if user["active"] else "Inactive"}
