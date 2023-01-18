from fastapi import FastAPI, Depends, Response, status, Request
from fastapi.responses import JSONResponse
import models
from database import SessionLocal, engine, Base
from sqlalchemy.orm import Session
from pydantic import BaseModel
from starlette_validation_uploadfile import ValidateUploadFileMiddleware
from sqlalchemy import text


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
        ValidateUploadFileMiddleware,
        app_path="/upload/",
        file_type="text/csv"
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class UserSchema(BaseModel):
    name: str
    age: int
    grade: str

    class Config:
        orm_mode = True


@app.post("/upload")
async def handleform(request: Request, response: Response):
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Origin"] = "*"
    form = await request.form()
    content_type = form[next(iter(form))].content_type
    filename = form["file"].filename
    contents = await form["file"].read()

    conn = engine.connect()
    sql_text = text( "SELECT * FROM public.\"Student\"")
    result = conn.execute(sql_text)
    print(filename)
    print(contents)
    print(result)
    if filename[-4:] == ".csv":
        return {
            contents,   
            content_type
            }
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error":"File isn't CSV"}

@app.get("/main", response_class=JSONResponse)
def stud_details(response: Response, db: Session = Depends(get_db)):
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return db.query(models.Student).all()


@app.post("/main", response_model=UserSchema)
def create_stud(stud: UserSchema, db: Session = Depends(get_db)):
    s = models.Student(name=stud.name, age=stud.age, grade=stud.grade)
    db.add(s)
    db.commit()
    return s


@app.put("/main/{stud_id}")
def update_stud(stud_id: int, stud: UserSchema, db: Session = Depends(get_db)):
    try:
        s = db.query(models.Student).filter(
            models.Student.id == stud_id).first()
        s.name = stud.name
        s.age = stud.age
        s.grade = stud.grade
        db.add(s)
        db.commit()
        return s
    except:
        return ("Student Not Found!")


@app.delete("/main/{stud_id}", response_class=JSONResponse)
def delete_stud(stud_id: int, stud: UserSchema, db: Session = Depends(get_db)):
    try:
        s = db.query(models.Student).filter(
            models.Student.id == stud_id).first()
        db.delete(s)
        db.commit()
        return {f"Student of id {stud_id} has been deleted": True}
    except:
        return ("Student Not Found!")
