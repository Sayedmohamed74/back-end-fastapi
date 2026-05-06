from fastapi import FastAPI
from api import auth, students, parents, staff


app = FastAPI()


app.include_router(auth.router)
app.include_router(students.router)
app.include_router(parents.router)
app.include_router(staff.router)
