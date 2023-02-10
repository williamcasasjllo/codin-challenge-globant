-- Challenge 2 Requirement 1
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

-- Challenge 2 Requirement 2
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