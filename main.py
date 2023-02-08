from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

class Employee(BaseModel):
    id: int                     # Id of the employee
    name: str                   # Name and surname of the employee
    datetime: str               # Hire datetime in ISO format
    department_id: int          # Id of the department which the employee was hired for
    job_id: int                 # Id of the job which the employee was hired for

class EmployeeList(BaseModel):
    data: List[Employee]        # List of employees

class Department(BaseModel):
    id: int                     # Id of the department
    department: str             # Name of the department

class DepartmentList(BaseModel):
    data: List[Department]      # List of departments

class Job(BaseModel):
    id: int                     # Id of the job
    job: str                    # Name of the job

class JobList(BaseModel):
    data: List[Job]             # List of jobs

app = FastAPI()

@app.post("/employee/")
async def create_employee(employee: Employee):
    return employee

@app.post("/employeeList")
async def create_employees(employee_list: EmployeeList):
    return employee_list

@app.post("/department/")
async def create_department(department: Department):
    return department

@app.post("/departmentList")
async def create_departments(department_list: DepartmentList):
    return department_list

@app.post("/job/")
async def create_job(job: Job):
    return job

@app.post("/jobList")
async def create_departments(job_list: JobList):
    return job_list


# uvicorn main:app --reload