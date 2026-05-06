from fastapi import APIRouter, Body, HTTPException, Depends, Query
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from repositories.student_repo import StudentRepo
from repositories.parents_repo import ParentsRepo
from repositories.staff_repo import StaffRepo
from core.database import get_db
from enum import Enum
from core.auth import (
    convert_pass_hash,
    convert_info_token,
    convert_token_info,
    DUMMY_HASH,
    compare_pass_hash,
    get_user,
)


class RegisterStudent(BaseModel):
    userName: str
    password: str
    email: EmailStr
    birthDate: datetime
    gender: str
    created_at: str = datetime.now(timezone.utc).isoformat()


class RegisterParents(BaseModel):
    userName: str
    password: str
    email: EmailStr
    phoneNumber: str


class ResponseRegister(BaseModel):
    created: bool


class DataOfToken(BaseModel):
    userName: str
    email: EmailStr
    gender: str
    created_at: str


class ReturnUser(BaseModel):
    userName: str
    email: EmailStr
    birthDate: str
    gender: str
    token: str
    id: int


class LoginUser(BaseModel):
    email: EmailStr
    password: str


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register/student", response_model=ResponseRegister)
async def register(data_user: Annotated[RegisterStudent, Body()], db=Depends(get_db)):
    repo = StudentRepo(db)
    student = repo.get_student_by_email(data_user.email.strip())

    if student:
        raise HTTPException(status_code=400, detail="This email is found")

    if not data_user.email.strip().isascii():
        raise HTTPException(
            status_code=400, detail="Email must contain English characters only"
        )

    try:
        password = convert_pass_hash(data_user.password)
        data_user.password = password
        repo.create_student(
            student_data={
                "name": data_user.userName,
                "email": data_user.email,
                "password": data_user.password,
                "birth_date": str(data_user.birthDate),
                "gender": data_user.gender,
                "created_at": data_user.created_at,
            }
        )
    except:
        raise HTTPException(
            status_code=500, detail="An error occurred while creating the student"
        )

    return ResponseRegister(created=True)


@router.post("/register/parents", response_model=ResponseRegister)
async def register(data_user: Annotated[RegisterParents, Body()], db=Depends(get_db)):
    repo = ParentsRepo(db)
    parent = repo.get_parents_by_email(data_user.email.strip())
    print("=" * 50)
    print(parent)

    if parent:
        raise HTTPException(status_code=400, detail="This email is found")

    if not data_user.email.strip().isascii():
        raise HTTPException(
            status_code=400, detail="Email must contain English characters only"
        )

    try:
        print("=" * 50)
        password = convert_pass_hash(data_user.password)
        print("=" * 50)
        data_user.password = password
        print("=" * 50)
        repo.create_parents(
            parents_data={
                "name": data_user.userName,
                "email": data_user.email,
                "password": data_user.password,
                "phone": data_user.phoneNumber,
            }
        )
        print("=" * 50)
    except:
        raise HTTPException(
            status_code=500, detail="An error occurred while creating the parent"
        )

    return ResponseRegister(created=True)


@router.post("/login")
async def get_token(user: LoginUser, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # data = convert_token_info(token)
        # if not data:
        #     raise credentials_exception
        repo_student = StudentRepo(db)
        repo_parents = ParentsRepo(db)
        repo_staff = StaffRepo(db)
        user_current = (
            repo_student.get_student_by_email(user.email.strip())
            or repo_parents.get_parents_by_email(user.email.strip())
            or repo_staff.get_staff_by_eamil(email=user.email.strip())
        )

        if not user_current:
            raise credentials_exception
        if not compare_pass_hash(user.password, user_current.password):
            raise credentials_exception

        if user_current.__table__.name == "students":
            token_payload = convert_info_token(
                {
                    "user_info": {
                        "id": user_current.id,
                        "name": user_current.name,
                        "email": user_current.email,
                        "birth_date": str(user_current.birth_date),
                        "gender": user_current.gender,
                        "quran": user_current.quran_progress,
                        "package": user_current.monthly_package,
                        "is_student": False,
                    }
                }
            )
        elif user_current.__table__.name == "parents":
            token_payload = convert_info_token(
                {
                    "user_info": {
                        "id": user_current.id,
                        "name": user_current.name,
                        "email": user_current.email,
                        "is_parent": True,
                    }
                }
            )
        else:
            token_payload = convert_info_token(
                {
                    "user_info": {
                        "id": user_current.id,
                        "name": user_current.name,
                        "email": user_current.email,
                        "is_parent": False,
                        "role": user_current.role,
                        "gender": user_current.gender,
                    }
                }
            )

        print(token_payload)

        return token_payload

    except Exception as e:
        raise credentials_exception


@router.get("/getUser")
async def get_me(user=Depends(get_user)):
    return user


@router.post("/tokens", include_in_schema=False)
async def login(
    user: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print(user.username)
    repo_student = StudentRepo(db)
    repo_parents = ParentsRepo(db)
    repo_staff = StaffRepo(db)
    user_current = (
        repo_student.get_student_by_email(user.username.strip())
        or repo_parents.get_parents_by_email(user.username.strip())
        or repo_staff.get_staff_by_eamil(user.username.strip())
    )

    print(user_current)
    try:
        # data = convert_token_info(token)
        # if not data:
        #     raise credentials_exception

        if not user_current:
            raise credentials_exception
        if not compare_pass_hash(user.password, user_current.password):
            raise credentials_exception

        if user_current.__table__.name == "students":
            token_payload = convert_info_token(
                {
                    "user_info": {
                        "id": user_current.id,
                        "name": user_current.name,
                        "email": user_current.email,
                        "birth_date": str(user_current.birth_date),
                        "gender": user_current.gender,
                        "quran": user_current.quran_progress,
                        "package": user_current.monthly_package,
                        "is_student": False,
                    }
                }
            )
        elif user_current.__table__.name == "parents":
            token_payload = convert_info_token(
                {
                    "user_info": {
                        "id": user_current.id,
                        "name": user_current.name,
                        "email": user_current.email,
                        "is_parent": True,
                    }
                }
            )
        else:
            token_payload = convert_info_token(
                {
                    "user_info": {
                        "id": user_current.id,
                        "name": user_current.name,
                        "email": user_current.email,
                        "is_parent": False,
                        "role": user_current.role,
                        "gender": user_current.gender,
                    }
                }
            )

        print(token_payload)

        return {"access_token": token_payload["token"], "token_type": "bearer"}

    except Exception as e:
        raise credentials_exception
