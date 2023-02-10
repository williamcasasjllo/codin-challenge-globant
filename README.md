# Globant Coding Challenge #

- [Globant Coding Challenge](#globant-coding-challenge)
- [Components and Libraries](#components-and-libraries)
  - [Components](#components)
  - [Libraries](#libraries)
- [ETL Resources](#etl-resources)
- [ETL Functions](#etl-functions)
- [API Resources](#api-resources)
- [Database Components](#database-components)
  - [Script to create employees table](#script-to-create-employees-table)
  - [Script to create departments table](#script-to-create-departments-table)
  - [Script to create jobs table](#script-to-create-jobs-table)
- [Knime Features](#knime-features)
  - [Backup in AVRO format](#backup-in-avro-format)
  - [Restore backup with AVRO files](#restore-backup-with-avro-files)
- [Challenge 2 Requirements](#challenge-2-requirements)
  - [Requirement 1](#requirement-1)
  - [Requirement 2](#requirement-2)



# Components and Libraries

## Components

- Python (Version 3.9.7) (Versioned with virtualenv 3.9.7)
- Microsoft SQL Server 2016 (SP2-CU15-GDR) (KB4583461)
- Knime (Version 4.1.2)

## Libraries

List of Python libraries needed to install:

- datetime (native)
- fastapi==0.89.1
- json (native)
- numpy==1.20.3
- pandas==1.3.5
- pathlib (native)
- pydantic==1.10.4
- requests==2.26.0
- SQLAlchemy==2.0.2
- urllib3==1.26.7


# ETL Resources

ETL file: monitor_files.py
This script reads the CSV files and send it to the service to store the data on database. Endpoints used on this script writes on database on a bulk petition.

Next code on the script let to send retries to the service if it fails or returns a bad status.

```python
SESSION = requests.session()
retry = Retry(total=3, backoff_factor=1, status_forcelist=[
              400, 413, 429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
SESSION.mount("http://", adapter)
SESSION.mount("https://", adapter)
```

Next variables need to be seted with absolute path on code to read the CSV files: 

```python
FILE_EMPLOYEE_PATH
FILE_DEPARTMENT_PATH
FILE_JOBS_PATH
```

# ETL Functions

- main(): Start the process and invoke the *process_file* function.
- process_file(filepath, model, endpoint): Function that process the file to execute transformations functions and send the data to database. It checks if there's a file to process and if it exists transform on a pandas dataframe and start to execute the functions. This function use nexts parameter:
  - filepath: Path file variable where the CSV is stored.
  - model: Name of the model to process. Values: Employees, Departments or Jobs.
  - endpoint: Name of the endpoint api rest service to send the data. Values: employeeList, departmentList, jobList.
- df_to_list(dataframe): Checks if dataframe has *nan* values and replace *nan* for *None*. Also transform the pandas dataframe on a list of values.
- remove_error_data(data): This function takes each row of the dataset to check if all values exists. If all the values of the row exists, it append the register on a new list, else, print the error row on a log.
- list_to_dict(list_data, type): Transform the las list on a list of dictionaries to send it via API Service.
- send_data(data, endpoint): This function takes all the data and send it to the API services.



# API Resources

API Service is on a FastAPI frameworks.

To start the service, need to be on the folder where main.py is located, and then execute next command:
```bash
uvicorn main:app --reload
```

When the service is running you can visit the API documentation with the next links:
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

The service has the option to send values by one or send a bulk of data with one request.

# Database Components

There are three database tables where the solution stores the data: 

```sql
SELECT * FROM dbo.employees
SELECT * FROM dbo.departments
SELECT * FROM dbo.jobs
```
## Script to create employees table
```sql
USE <databasename>
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[employees](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[name] [varchar](255) NULL,
	[datetime] [varchar](255) NULL,
	[department_id] [int] NULL,
	[job_id] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
```

## Script to create departments table
```sql
USE <databasename>
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[departments](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[department] [varchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
```

## Script to create jobs table
```sql
USE <databasename>
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[jobs](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[job] [varchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
```

# Knime Features

There are two special features stored in */files/features*:
https://github.com/williamcasasjllo/codin-challenge-globant/tree/main/files/features

Backups are stored on */files/avro/backups* path:
https://github.com/williamcasasjllo/codin-challenge-globant/tree/main/files/avro/backups

## Backup in AVRO format


Knime workflow *BACKUP_DB_AVRO_FORMAT_V1.knwf* let to get the data from tables and write on a AVRO format.

## Restore backup with AVRO files

Knime workflow *RESTORE_BACKUP_AVRO_FORMAT_V1.knwf* let to get the data from avro files (First you need to set up the name of backup file). If there's data on avro file, it delete the data on the specific table database and then, write the backup data on the database.

# Challenge 2 Requirements

The FastAPI service have two endpoints to get the data

## Requirement 1

Service http://127.0.0.1:8000/employeesHiredByQuarter/ returns the information of employees hired by quarter on 2021 year.

## Requirement 2

Service http://127.0.0.1:8000/hiredEmployeesByDepartment/ returns the information of hired employees by department on 2021 year.

Visit documentation to get more information
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc 