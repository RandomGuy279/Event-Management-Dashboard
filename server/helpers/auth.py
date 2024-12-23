import jwt
from datetime import datetime, timedelta
from typing import Union
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from .logger_setup import logger
from .config import configData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to create JWT token
def create_access_token(data: dict, expires_in: Union[int, timedelta] = configData["jwtSettings"]["accessTokenExpireMinutes"]):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=expires_in)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, key=configData["jwtSettings"]["secretKey"], algorithm=configData["jwtSettings"]["algorithm"])
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating JWT token: {e}")
        raise Exception(f"An error occurred while creating the token: {e}")

# Function to decode JWT token
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, configData["jwtSettings"]["secretKey"], algorithms=[configData["jwtSettings"]["algorithm"]])
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token has expired.")
        raise Exception("Token has expired.")
    except jwt.PyJWTError as e:
        logger.error(f"JWT token decoding failed: {e}")
        raise Exception("Invalid token.")
    except Exception as e:
        logger.error(f"Error verifying JWT token: {e}")
        raise Exception(f"An error occurred while verifying the token: {e}")
    
# Dependency to verify JWT token
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    return payload