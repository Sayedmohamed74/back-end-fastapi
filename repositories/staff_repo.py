from sqlalchemy.orm import Session
from sqlalchemy import text
from models.models import Parents, Staff, Students


class StaffRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_staff_by_eamil(self, email: str):
        self.db.execute(text(f"set local app.email='{email}'"))
        self.db.execute(text("set local app.user_id='0'"))
        self.db.execute(text("set local app.role=''"))
        user = self.db.query(Staff).first()
        return user

    def get_staff_all(self, role, id):
        self.db.execute(text(f"set local app.user_id='{id}'"))
        self.db.execute(text(f"set local app.role='{role}'"))
        return self.db.query(Staff).all()

    def get_students(self, role, id):
        self.db.execute(text(f"set local app.user_id='{id}'"))
        self.db.execute(text(f"set local app.role='{role}'"))
        if role == "admin":
            return self.db.query(Students).all()
        elif role == "supervisor":
            staff = self.db.query(Staff).all()
            return [li for stu in staff for li in stu.students]
        else:
            return self.db.query(Students).filter(Students.teacher_id == id)

    def add_parent(self, data):
        return self.db.add(**data)

    def add_staff(self, data):
        return self.db.add(**data)

    def get_all_parents(self):
        return self.db.query(Parents).all()
