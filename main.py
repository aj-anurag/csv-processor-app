from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class UserSchema(BaseModel):
    name:str
    age:int
    grade:str
    class Config:
        orm_mode=True


@app.get("/main")
def stud_details(db:Session = Depends(get_db)):
    return db.query(models.Student).all()
   
@app.post("/main", response_model=UserSchema)
def create_stud(stud:UserSchema, db:Session = Depends(get_db)):
    s = models.Student(name = stud.name, age = stud.age, grade = stud.grade)
    db.add(s)
    db.commit()
    return s

@app.put("/main/{stud_id}")
def update_stud(stud_id:int, stud:UserSchema, db:Session = Depends(get_db)):
    try:
        s =db.query(models.Student).filter(models.Student.id==stud_id).first()
        s.name=stud.name
        s.age=stud.age
        s.grade=stud.grade
        db.add(s)
        db.commit()
        return s
    except:
        return ("Student Not Found!")

@app.delete("/main/{stud_id}", response_class=JSONResponse)
def delete_stud(stud_id:int, stud:UserSchema, db:Session = Depends(get_db)):
    try:
        s =db.query(models.Student).filter(models.Student.id==stud_id).first()
        db.delete(s)
        db.commit()
        return{f"Student of id {stud_id} has been deleted":True}
    except:
        return ("Student Not Found!")

