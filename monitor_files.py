import pandas as pd
import numpy as np
import requests
import json
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import time
from datetime import datetime
from pathlib import Path

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
    dataframe = dataframe.replace({np.nan:None})
    list_values = dataframe.values.tolist()
    return list_values


def remove_error_data(data):
    response = []
    for row in data:
        check = any(x is None for x in row)
        if check == True:
            print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                  '-- Error on row with: ', row),' have None value --'
        else:
            print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                  '-- Row correct: ', row, ' --')
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
                "department": data[1]
            }
            list_dict.append(department)

    elif type == 'Jobs':
        for data in list_data:
            job = {
                "id": data[0],
                "job": data[1]
            }
            list_dict.append(job)

    return list_dict


def send_data(data, endpoint):

    url = 'http://127.0.0.1:8000/' + endpoint + '/'
    payload = json.dumps({
        "data": data
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = SESSION.request(
            "POST", url, headers=headers, data=payload, verify=False)
        print(response.text)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)


def process_file(filepath, model, endpoint):
    if Path(filepath).is_file():
        dataframe = pd.read_csv(filepath, header=None)
        list_data = df_to_list(dataframe)
        list_data = remove_error_data(list_data)
        list_dict_data = list_to_dict(list_data, model)
        send_data(list_dict_data, endpoint)
    else:
        print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +
              '-- File:' + filepath + 'no detected --')


def main():
    start_time = time.time()
    print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' -- Start --')
    process_file(FILE_EMPLOYEE_PATH, model='Employees',
                 endpoint='employeeList')
    process_file(FILE_DEPARTMENT_PATH, model='Departments',
                 endpoint='departmentList')
    process_file(FILE_JOBS_PATH, model='Jobs', endpoint='jobList')
    print('-- Execution time: %s seconds' % (time.time() - start_time))


if __name__ == '__main__':
    main()
