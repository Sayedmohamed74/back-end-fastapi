from repositories.staff_repo import StaffRepo


class StaffServices:
    def __init__(self, repo):
        self.repo: StaffRepo = repo

    def get_all(self):
        pass
