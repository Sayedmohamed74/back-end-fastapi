from sqlalchemy.orm import Session
from sqlalchemy import text
from models.models import Schedules, Staff, Students


class SchedulesRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_all_schedules(self, role, id):
        self.db.execute(text(f"set local app.user_id='{id}'"))
        self.db.execute(text(f"set local app.role='{role}'"))
        if role == "admin":
            staff = self.db.query(Staff).all()
            respons = []

            for st in staff:
                list = st.schedules
                list_of_sch = []
                for li in list:
                    list_of_sch.append(
                        {
                            "name": li.student.name,
                            "start": li.start_time,
                            "end": li.end_time,
                        }
                    )
                respons.append({"name": st.name, "list": list_of_sch})
            return respons

        elif role == "teacher":
            staff = self.db.query(Staff)
            respons = []

            for st in staff:
                list = st.schedules
                list_of_sch = []
                for li in list:
                    list_of_sch.append(
                        {
                            "name": li.student.name,
                            "start": li.start_time,
                            "end": li.end_time,
                        }
                    )
                respons.append({"name": st.name, "list": list_of_sch})
            return respons
        elif role == "supervisor":
            staff = self.db.query(Staff).filter(Staff.supervisor_id == id)
            respons = []

            for st in staff:
                list = st.schedules
                list_of_sch = []
                for li in list:
                    list_of_sch.append(
                        {
                            "name": li.student.name,
                            "start": li.start_time,
                            "end": li.end_time,
                        }
                    )
                respons.append({"name": st.name, "list": list_of_sch})
            return respons

    def set_schedules(self, role, id, schedules):
        if role == "teacher":
            new_schedules = Schedules(**schedules)
            self.db.add(new_schedules)
            self.db.commit()
            self.db.refresh(new_schedules)
