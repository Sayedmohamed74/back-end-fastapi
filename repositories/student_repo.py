from sqlalchemy.orm import Session
from models.models import Students


class StudentRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_all_students(self):
        return self.db.query(Students)

    def get_student_by_id(self, student_id: int):
        return self.db.query(Students).filter(Students.id == student_id).first()

    def get_student_by_email(self, email: str):
        return self.db.query(Students).filter(Students.email == email).first()

    def get_student_for_teacher(self, teacher_id: int):
        return self.db.query(Students).filter(Students.teacher_id == teacher_id).all()

    def get_student_for_parent(self, parent_id: int):
        return self.db.query(Students).filter(Students.parent_id == parent_id).all()

    def create_student(self, student_data: Students):
        new_student = Students(**student_data)
        self.db.add(new_student)
        self.save(new_student)

    def updata_student(self, id, data):
        self.db.query(Students).filter(id == Students.id).update(data)
        self.db.commit()
        return self.db.query(Students).filter(Students.id == id).first()

    def delete_student(self, student):

        self.db.delete(student)
        self.db.commit()

    def save(self, new):
        self.db.commit()
        self.db.refresh(new)
