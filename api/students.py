from datetime import date, datetime
from typing import Optional, TypedDict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr, BaseModel

from core.auth import get_user
from core.database import get_db
from repositories.student_repo import StudentRepo
from services.student_services import StudentService

router = APIRouter(prefix="/student", tags=["student"])


class ResopenseStudent(BaseModel):
    gender: Optional[str]
    monthly_package: Optional[float]
    teacher_id: Optional[int]
    name: Optional[str]
    email: Optional[EmailStr]
    birth_date: Optional[date]
    quran_progress: Optional[float]
    parent_id: Optional[int]
    created_at: Optional[datetime]


class RequestStudent(BaseModel):
    gender: Optional[str] = None
    monthly_package: Optional[float] = None

    name: Optional[str] = None

    birth_date: Optional[date] = None
    quran_progress: Optional[float] = None


@router.get("/self", response_model=ResopenseStudent)
async def get_students(user=Depends(get_user), db=Depends(get_db)):

    try:
        print(user)
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if user["user_info"]["is_parent"]:
            raise HTTPException(status_code=403, detail="Forbidden")
        repo = StudentRepo(db)
        service = StudentService(repo)
        return service.show_student_for_self(user["user_info"]["id"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/edit", response_model=ResopenseStudent)
async def edit_student(
    data: RequestStudent, user=Depends(get_user), db=Depends(get_db)
):
    try:
        print(user)
        print("================================")
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if user["user_info"]["is_parent"]:
            raise HTTPException(status_code=403, detail="Forbidden")
        repo = StudentRepo(db)
        result = repo.updata_student(data=data.model_dump(), id=user["user_info"]["id"])
        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete")
async def delete_student(user=Depends(get_user), db=Depends(get_db)):
    print("==============+++++++")
    repo = StudentRepo(db)
    service = StudentService(repo)
    try:
        print(user)
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if user["user_info"]["is_parent"]:
            raise HTTPException(status_code=403, detail="Forbidden")
        print("==============")
        repo = StudentRepo(db)
        print("==============")
        service = StudentService(repo)
        print("==============")

        return service.remove_student(user["user_info"]["id"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
