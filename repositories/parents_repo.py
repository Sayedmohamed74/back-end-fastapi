from models.models import Parents


class ParentsRepo:
    def __init__(self, db):
        self.db = db

    def get_parents_by_email(self, email: str):
        return self.db.query(Parents).filter(Parents.email == email).first()

    def create_parents(self, parents_data):

        new_parents = Parents(**parents_data)
        self.db.add(new_parents)

        self.save(new_parents)

    def save(self, obj):
        self.db.commit()
        self.db.refresh(obj)
