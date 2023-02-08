import pandas as pd
import requests
import json
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import time
from datetime import datetime
from pathlib import Path
import pyodbc

SESSION = requests.session()
retry = Retry(total=3, backoff_factor=1, status_forcelist=[
              400, 413, 429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
SESSION.mount("http://", adapter)
SESSION.mount("https://", adapter)

FILE_EMPLOYEE_PATH = 'D:\\REPOSITORIOS\\codin-challenge-globant\\files\\new\\hired_employees.csv'
FILE_DEPARTMENT_PATH = 'D:\\REPOSITORIOS\\codin-challenge-globant\\files\\new\\departments.csv'
FILE_JOBS_PATH = 'D:\\REPOSITORIOS\\codin-challenge-globant\\files\\new\\jobs.csv'


def df_to_list(dataframe):
    dataframe = dataframe.where(pd.notnull(dataframe), None)
    list_values = dataframe.values.tolist()
    return list_values


def remove_error_data(data):
    response = []
    for row in data:
        check = any(x is None for x in row)
        if check == True:
            print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                  ' -- Error on row with: ', row)
        else:
            print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                  ' -- Row correct: ', row)
            response.append(row)

    return response


def list_to_dict(list_data, type):
    list_dict = []
    if type == 'Employees':
        for data in list_data:
            employee = {
                "id": data[0],
                "name": data[1],
                "datetime": data[2],
                "department_id": data[3],
                "job_id": data[4]
            }
            list_dict.append(employee)

    elif type == 'Departments':
        for data in list_data:
            department = {
                "id": data[0],
                "employee_name": data[1],
                "datetime": data[2],
                "department_id": data[3],
                "job_id": data[4]
            }
            list_dict.append(department)

    elif type == 'Jobs':
        for data in list_data:
            job = {
                "id": data[0],
                "employee_name": data[1],
                "datetime": data[2],
                "department_id": data[3],
                "job_id": data[4]
            }
            list_dict.append(job)

    return list_dict


def send_data(data):
    url = "http://127.0.0.1:8000/employeeList/"

    payload = json.dumps({
        "data": data
    })
    headers = {
        'Content-Type': 'application/json'
    }
    print(payload)
    response = SESSION.request(
        "POST", url, headers=headers, data=payload, verify=False)
    print(response.text)


def main():
    start_time = time.time()
    print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' -- Start --')

    if Path(FILE_EMPLOYEE_PATH).is_file():
        df_employees = pd.read_csv(FILE_EMPLOYEE_PATH, header=None)
        list_employees = df_to_list(df_employees)
        list_employees = remove_error_data(list_employees)
        list_dict_employees = list_to_dict(list_employees, 'Employees')
        send_data(list_dict_employees)
    else:
        print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +
              ' -- No hired_employees file detected --')
    
    print('-- Execution time: %s seconds' % (time.time() - start_time))


'''
    if Path(FILE_DEPARTMENT_PATH).is_file():
        df_departments = pd.read_csv(FILE_DEPARTMENT_PATH)
        list_departments = pandas_to_list(df_departments)
        list_departments = check_data(list_departments)
    else:
        print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' -- No departments file detected --')

    if Path(FILE_JOBS_PATH).is_file():
        df_jobs = pd.read_csv(FILE_JOBS_PATH)
        list_jobs = pandas_to_list(df_jobs)
        list_jobs = check_data(list_jobs)
    else:
        print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' -- No jobs file detected --')
'''
    

if __name__ == '__main__':
    main()
