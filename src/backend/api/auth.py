import jwt
from os import getenv
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

ALGORITHM = "HS256"

def is_token_valid(token: str):
    if check_token(token):
        return True
    else:
        raise HTTPException(status_code=401, detail="Invalid API key")

def check_token(token: str):
    if token == getenv("API_KEY"):
        return True
    else:
        return False