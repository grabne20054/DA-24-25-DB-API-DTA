import jwt
from os import getenv
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

ALGORITHM = "HS256"

def decode_jwt_token(token: str, verify_expiration: bool):
    decoded_token = jwt.decode(token, getenv("JWT_SECRET_KEY"), algorithms=[ALGORITHM], options={"verify_exp": verify_expiration})
    return decoded_token

def is_token_valid(token: str):
    try:
        decode_jwt_token(token, verify_expiration=True)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return True