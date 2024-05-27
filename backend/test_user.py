from fastapi import FastAPI,Depends
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app
from routers import user as user_router 
from passlib.context import CryptContext
from hashing import Hash
import json
import random




client = TestClient(app)
app.include_router(user_router.router)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Reachy"}

def test_create_user():
    request_data = {
        "name": "testuser",
        "email": "test@gmail.com",
        "password": "12345"
    }
    text_content = json.dumps(request_data)

    response = client.post("/user/",content = text_content)
    pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


    assert response.status_code == 200
    assert response.json()["user"]["name"] == "testuser"
    assert response.json()["user"]["email"] == "test@gmail.com"
    assert pwd_cxt.verify(request_data["password"], response.json()["user"]["password"])
    global id
    id = response.json()["user"]["id"]

def test_create_user_email_already_in_use():
    request_data = {
        "name": "testuser",
        "email": "test@gmail.com",
        "password": "12345"
    }
    text_content = json.dumps(request_data)

    response = client.post("/user/",content = text_content)

    assert response.status_code == 404
    assert response.json()["detail"] == "Email already in use"
    
# positive test for login 
def test_login():
    data = {
    "grant_type": "",
    "username": "test@gmail.com",
    "password": "12345",
    "scope": "",
    "client_id": "",
    "client_secret": ""
    }
    headers = {
    "Content-Type": "application/x-www-form-urlencoded"
    }

    # Convert the data dictionary to a form-encoded string
    encoded_data = "&".join(f"{key}={value}" for key, value in data.items())
    response = client.post("/login",headers=headers, content=encoded_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    global access_token
    access_token = response.json()["access_token"]

# negative test for login (invalid password)
def test_login_invalid_password():
    data = {
    "grant_type": "",
    "username": "test@gmail.com",
    "password": "123",
    "scope": "",
    "client_id": "",
    "client_secret": ""
    }
    headers = {
    "Content-Type": "application/x-www-form-urlencoded"
    }

    # Convert the data dictionary to a form-encoded string
    encoded_data = "&".join(f"{key}={value}" for key, value in data.items())
    response = client.post("/login",headers=headers, content=encoded_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Invalid Credentials"

# negative test for login (invalid email)
def test_login_invalid_email():
    data = {
    "grant_type": "",
    "username": "test@",
    "password": "123",
    "scope": "",
    "client_id": "",
    "client_secret": ""
    }
    headers = {
    "Content-Type": "application/x-www-form-urlencoded"
    }

    # Convert the data dictionary to a form-encoded string
    encoded_data = "&".join(f"{key}={value}" for key, value in data.items())
    response = client.post("/login",headers=headers, content=encoded_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Invalid Credentials"

# negative test for login (null email and null password)
def test_login_invalid_email_and_password():
    data = {
    "grant_type": "",
    "username": " ",
    "password": " ",
    "scope": "",
    "client_id": "",
    "client_secret": ""
    }
    headers = {
    "Content-Type": "application/x-www-form-urlencoded"
    }

    # Convert the data dictionary to a form-encoded string
    encoded_data = "&".join(f"{key}={value}" for key, value in data.items())
    response = client.post("/login",headers=headers, content=encoded_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Invalid Credentials"
 
    
# test for getting current user data
def test_get_me():
    response = client.get("/user/me",headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["id"] == id
    assert response.json()["name"] == "testuser"
    assert response.json()["email"] == "test@gmail.com"
    assert "followings" in response.json()
    assert "followers" in response.json()
    assert "friends_count" in response.json()

# test: get user by id
def test_get_user():
    user_id = random.randint(1, id)

    response = client.get(f"/user/{user_id}",headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["id"] == user_id
    assert "name" in response.json()
    assert "email" in response.json()
    assert "followings" in response.json()
    assert "followers" in response.json()
    assert "friends_count" in response.json()

#test for deleting user
def test_destroy():
    response = client.delete(f"/user/{id}",headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 204  # No Content
    


    




