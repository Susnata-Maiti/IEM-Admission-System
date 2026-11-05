"""
Authentication and Role-Based Access Control (RBAC) Module
Implements FR-01, FR-02, FR-14 and NFR-02 (Salted password hashing & JWT/token RBAC).
"""

import hmac
import hashlib
import base64
import json
import time
import re
from fastapi import HTTPException, Header, Depends

SECRET_KEY = os.environ["SECRET_KEY"]


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    FR-01: Passwords must be a minimum of 8 characters and contain
    at least one uppercase letter and at least one special character.
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>\-_=+/~`]", password):
        return False, "Password must contain at least one special character."
    return True, ""


def create_access_token(user_id: int, email: str, role: str, name: str) -> str:
    """Generates an HMAC-SHA256 signed access token (JWT format)."""
    payload = {
        "user_id": user_id,
        "email": email,
        "role": role,
        "name": name,
        "exp": int(time.time()) + 86400  # 24 hours
    }
    header = {"alg": "HS256", "typ": "JWT"}
    
    b64_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    b64_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    
    signature = hmac.new(
        SECRET_KEY.encode(),
        f"{b64_header}.{b64_payload}".encode(),
        hashlib.sha256
    ).digest()
    b64_sig = base64.urlsafe_b64encode(signature).decode().rstrip("=")
    
    return f"{b64_header}.{b64_payload}.{b64_sig}"


def decode_access_token(token: str) -> dict:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            raise HTTPException(status_code=401, detail="Invalid token structure")
        
        b64_header, b64_payload, b64_sig = parts
        
        expected_sig = hmac.new(
            SECRET_KEY.encode(),
            f"{b64_header}.{b64_payload}".encode(),
            hashlib.sha256
        ).digest()
        actual_sig = base64.urlsafe_b64decode(b64_sig + "=="[:(4 - len(b64_sig) % 4) % 4])
        
        if not hmac.compare_digest(expected_sig, actual_sig):
            raise HTTPException(status_code=401, detail="Invalid token signature")
        
        payload_json = base64.urlsafe_b64decode(b64_payload + "=="[:(4 - len(b64_payload) % 4) % 4])
        payload = json.loads(payload_json)
        
        if payload.get("exp", 0) < time.time():
            raise HTTPException(status_code=401, detail="Token has expired")
            
        return payload
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication error: {str(e)}")


def get_current_user(authorization: str = Header(None)) -> dict:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    parts = authorization.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization scheme, expected 'Bearer <token>'")
    
    return decode_access_token(parts[1])


def require_roles(allowed_roles: list[str]):
    def role_checker(user: dict = Depends(get_current_user)) -> dict:
        if user.get("role") not in allowed_roles:
            raise HTTPException(
                status_code=403, 
                detail=f"Forbidden: Access restricted to roles {allowed_roles}. You are '{user.get('role')}'"
            )
        return user
    return role_checker
