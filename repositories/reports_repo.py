from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from models.models import Reports, Students


class ReportOut(BaseModel):
    report_text: Optional[str] = None
    quran_reached: Optional[str] = None


class ChildWithReports(BaseModel):
    name: str
    reports: List[ReportOut]


class ReportsRepo:
    def __init__(self, db: Session):
        self.db = db

    def reportes_for_parents(self, id: int):
        students = self.db.query(Students).filter(Students.parent_id == id).all()
        return [
            ChildWithReports(
                name=s.name,
                reports=[
                    ReportOut(report_text=r.report_text, quran_reached=r.quran_reached)
                    for r in s.reports
                ],
            )
            for s in students
        ]

    def set_repot(self, role, data):
        if role == "teacher":
            new_report = Reports(**data)
            self.db.add(new_report)
            self.db.commit()
            self.db.refresh(new_report)
