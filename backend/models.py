"""
Pydantic Request and Response Models for IEM Admission System
Handles strict validation according to SRS and Project Charter.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=5, max_length=100)
    password: str = Field(..., min_length=8)

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        v = v.strip().lower()
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", v):
            raise ValueError("Invalid email address format.")
        return v


class LoginRequest(BaseModel):
    email: str
    password: str


class ApplicationDraftRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    dob: str = Field(..., min_length=4)
    contact_number: str = Field(..., min_length=10, max_length=15)
    address: str = Field(..., min_length=5, max_length=250)
    class_10_marks: float = Field(..., ge=0.0, le=100.0)
    class_10_board: str = Field(..., min_length=2)
    class_12_marks: float = Field(..., ge=0.0, le=100.0)
    class_12_board: str = Field(..., min_length=2)
    passing_year: int = Field(..., ge=2015, le=2030)
    course: str = Field(..., min_length=2)

    @field_validator("contact_number")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        cleaned = re.sub(r"[^\d+]", "", v)
        if len(re.sub(r"[^\d]", "", cleaned)) < 10:
            raise ValueError("Contact number must contain at least 10 digits.")
        return v


class StatusUpdateRequest(BaseModel):
    new_status: str
    remarks: Optional[str] = ""
