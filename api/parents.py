from datetime import date, datetime
from typing import Optional, TypedDict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr, BaseModel

from core.auth import get_user
from core.database import get_db
from repositories.student_repo import StudentRepo
from repositories.reports_repo import ReportsRepo
from services.student_services import StudentService

router = APIRouter(prefix="/parent", tags=["parents"])


class child(BaseModel):
    name: str
    quran_progress: Optional[str] = None


@router.get("/my-children", response_model=list[child])
async def my_children(db=Depends(get_db), user=Depends(get_user)):

    if not user:
        raise HTTPException(status_code=400, detail="forbbdien")
    if user["user_info"]["id"] and user["user_info"]["is_parent"]:
        repo = StudentRepo(db)
        students = repo.get_student_for_parent(user["user_info"]["id"])

        return [child(name=s.name, quran_progress=s.quran_progress) for s in students]


@router.get("/reportes")
async def reportes(db=Depends(get_db), user=Depends(get_user)):
    repo = ReportsRepo(db)
    return repo.reportes_for_parents(user["user_info"]["id"])
