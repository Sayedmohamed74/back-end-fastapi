from datetime import date, datetime
from typing import Optional, TypedDict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr, BaseModel

from core.auth import get_user
from core.database import get_db
from repositories.staff_repo import StaffRepo
from repositories.schedules_repo import SchedulesRepo
from repositories.reports_repo import ReportsRepo
from services.student_services import StudentService

router = APIRouter(prefix="/staff", tags=["manager"])


class AddSchedules(BaseModel):
    staff_id: int
    student_id: int
    sat: bool = False
    sun: bool = False
    mon: bool = False
    tues: bool = False
    wednes: bool = False
    thurs: bool = False
    fri: bool = False
    end_time: datetime = datetime.now().isoformat()
    start_time: datetime = datetime.now().isoformat()


class AddReport(BaseModel):
    teacher_id: int
    student_id: int
    report_text: str
    quran_reached: str
    evaluation_grade: str
    created_at: datetime = datetime.now().isoformat()


@router.get("/all")
async def all_staff(user=Depends(get_user), db=Depends(get_db)):
    repo = StaffRepo(db)

    return repo.get_staff_all(
        role=user["user_info"]["role"], id=user["user_info"]["id"]
    )


@router.get("/schedules")
def get_all_schedules(user=Depends(get_user), db=Depends(get_db)):
    if "role" in user["user_info"]:
        repo = SchedulesRepo(db)
        return repo.get_all_schedules(
            user["user_info"]["role"], user["user_info"]["id"]
        )
    else:
        raise HTTPException(status_code=401, detail="unAuht")


@router.get("/students")
def get_all_students(user=Depends(get_user), db=Depends(get_db)):
    repo = StaffRepo(db)
    return repo.get_students("supervisor", 2)


@router.post("/add/schedules")
def set_schedules(item: AddSchedules, user=Depends(get_user), db=Depends(get_db)):

    repo = SchedulesRepo(db)
    # repo.set_schedules(user['user_info']['role'] ,user['user_info']['id'],item.model_dump())
    repo.set_schedules("teacher", 3, item.model_dump())
    return {"created": True}


@router.post("/add/repot")
def set_schedules(item: AddReport, user=Depends(get_user), db=Depends(get_db)):

    repo = ReportsRepo(db)
    # repo.set_schedules(user['user_info']['role'] ,user['user_info']['id'],item.model_dump())
    repo.set_repot("teacher", item.model_dump())
    return {"created": True}
