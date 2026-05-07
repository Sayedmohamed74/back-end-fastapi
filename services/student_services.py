from repositories.student_repo import StudentRepo


class StudentService:
    def __init__(self, repo):
        self.repo: StudentRepo = repo

    def show_all_students_for_staff(self):
        return self.repo.get_all_students()

    def show_student_for_teacher(self, teacher_id: int):

        return self.repo.get_student_for_teacher(teacher_id)

    # def add_student(self,data):
    #     pass

    def show_student_for_self(self, id: int):
        return self.repo.get_student_by_id(id)

    def remove_student(self, id: int):

        student = self.repo.get_student_by_id(id)

        if not student:
            raise Exception("Student not found")

        self.repo.delete_student(student)
        return student
