from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Boolean, Column, Float, String, Integer
import urllib
from utils.settings import Settings

# uvicorn main:app --reload
# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()

##### SQL Configuration #####
settings = Settings()
server = settings.db_host
database = settings.db_name
username = settings.db_user
password = settings.db_pass
driver = '{ODBC Driver 17 for SQL Server}'
params = urllib.parse.quote_plus('DRIVER='+driver+';SERVER='+server+';DATABASE=' +
                                 database+';UID='+username+';PWD=' + password+';Trusted_Connection=no')
engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

##### Class, Schemas, Model #####


class DBEmployee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    datetime = Column(String(255))
    department_id = Column(Integer)
    job_id = Column(Integer)


class Employee(BaseModel):
    id: int
    name: str
    datetime: str
    department_id: int
    job_id: int

    class Config:
        orm_mode = True


class EmployeeList(BaseModel):
    data: List[Employee]


class DBDepartment(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    department = Column(String(255))


class Department(BaseModel):
    id: int
    department: str

    class Config:
        orm_mode = True


class DepartmentList(BaseModel):
    data: List[Department]


class DBJob(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    job = Column(String(255))


class Job(BaseModel):
    id: int
    job: str

    class Config:
        orm_mode = True


class JobList(BaseModel):
    data: List[Job]


Base.metadata.create_all(bind=engine)


##### Routes #####


@app.post("/employee/", response_model=Employee)
def create_employee(employee: Employee, db: Session = Depends(get_db)):
    db_employee = DBEmployee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@app.post("/employeeList/", response_model=EmployeeList)
async def create_employees(employee_list: EmployeeList, db: Session = Depends(get_db)):
    employees = []
    for employee in employee_list.data:
        db_employee = DBEmployee(**employee.dict())
        employees.append(db_employee)

    db.bulk_save_objects(employees)
    db.commit()
    return employee_list


@app.post("/department/", response_model=Department)
def create_department(department: Department, db: Session = Depends(get_db)):
    db_department = DBDepartment(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


@app.post("/departmentList/", response_model=DepartmentList)
async def create_departments(department_list: DepartmentList, db: Session = Depends(get_db)):
    departments = []
    for department in department_list.data:
        db_department = DBDepartment(**department.dict())
        departments.append(db_department)

    db.bulk_save_objects(departments)
    db.commit()
    return department_list


@app.post("/job/", response_model=Job)
def create_job(job: Job, db: Session = Depends(get_db)):
    db_job = DBJob(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@app.post("/jobList/", response_model=JobList)
async def create_jobs(job_list: JobList, db: Session = Depends(get_db)):
    jobs = []
    for job in job_list.data:
        db_job = DBJob(**job.dict())
        jobs.append(db_job)

    db.bulk_save_objects(jobs)
    db.commit()
    return job_list


@app.get("/employeesHiredByQuarter/")
async def get_employees_hired_by_quarter(db: Session = Depends(get_db)):
    query = text('''
                    SELECT
                        t.department,
                        t.job,
                        SUM(t.Q1) AS Q1,
                        SUM(t.Q2) AS Q2,
                        SUM(t.Q3) AS Q3,
                        SUM(t.Q4) AS Q4
                        FROM (
                            SELECT
                                d.department,
                                j.job,
                                CASE
                                    WHEN DATEPART(QUARTER, CAST(LEFT(datetime, 10) AS date)) = 1 THEN 1
                                    ELSE 0
                                END AS Q1,
                                CASE
                                    WHEN DATEPART(QUARTER, CAST(LEFT(datetime, 10) AS date)) = 2 THEN 1
                                    ELSE 0
                                END AS Q2,
                                CASE
                                    WHEN DATEPART(QUARTER, CAST(LEFT(datetime, 10) AS date)) = 3 THEN 1
                                    ELSE 0
                                END AS Q3,
                                CASE
                                    WHEN DATEPART(QUARTER, CAST(LEFT(datetime, 10) AS date)) = 4 THEN 1
                                    ELSE 0
                                END AS Q4
                            FROM dbo.employees AS e
                            LEFT JOIN dbo.departments AS d
                            ON e.department_id = d.id
                            LEFT JOIN dbo.jobs AS j
                            ON e.job_id = j.id
                            WHERE DATEPART(YEAR, CAST(LEFT(datetime, 10) AS date)) = 2021) AS t
                        GROUP BY t.department, t.job
                        ORDER BY t.department ASC, t.job ASC
                    '''
                )
    responses = db.execute(query).fetchall()
    response_list = []
    for response in responses:
        response_list.append(response._mapping)
    return response_list

@app.get("/hiredEmployeesByDepartment/")
async def get_hired_employees_by_department(db: Session = Depends(get_db)):
    query = text('''
                    SELECT t2.id, t2.department, t2.hiredEmployees
                        FROM (
                            SELECT d.id, d.department, COUNT(e.id) AS 'hiredEmployees'
                                FROM dbo.departments AS d
                                LEFT JOIN dbo.employees AS e
                                ON d.id = e.department_id
                                WHERE DATEPART(YEAR, CAST(LEFT(datetime, 10) AS date)) = 2021
                                GROUP BY d.department, d.id
                            ) AS t2
                            WHERE t2.hiredEmployees > (
                                                        SELECT AVG(tavg.hiredEmployees) AS 'avgHiredEmployees'
                                                            FROM (
                                                                SELECT d.department, COUNT(e.id) AS 'hiredEmployees' FROM dbo.departments AS d
                                                                LEFT JOIN dbo.employees AS e
                                                                ON d.id = e.department_id
                                                                WHERE DATEPART(YEAR, CAST(LEFT(datetime, 10) AS date)) = 2021
                                                                GROUP BY d.department
                                                                ) AS tavg
                                                        )
                            ORDER BY t2.hiredEmployees DESC
                    '''
                )
    responses = db.execute(query).fetchall()
    response_list = []
    for response in responses:
        response_list.append(response._mapping)
    return response_list
    

