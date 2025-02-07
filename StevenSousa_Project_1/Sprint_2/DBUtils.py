"""
Author: Steven Sousa
Prof.: John Santore
Institution: Bridgewater State University - COMP490 - Senior Design & Development
Version: 06Feb2025

This program handles the creation of the PostgreSQL database utilized in Sprint 2. If a db already exists, it will do
 noting. Additionally, if a job_id already exists in the database, it won't add it again.
"""
from typing import Tuple
from psycopg import DatabaseError, Connection, Cursor, connect


def open_db(dbname: str, user: str, password: str, host: str, port: str) -> Tuple[Connection, Cursor]:
    """
    This function will open a connection to the PostgreSQL database.
    :param dbname: os.getenv('DB_NAME')
    :param user: os.getenv('DB_USER')
    :param password: os.getenv('DB_PASSWORD')
    :param host: os.getenv('DB_HOST')
    :param port: os.getenv('DB_PORT')
    :return: connection and cursor to the database
    """
    try:
        conn = connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = conn.cursor()
        return conn, cursor
    except(Exception, DatabaseError) as error:
        print(error)
        raise error


def close_db(conn: Connection, cursor: Cursor) -> None:
    """
    This function will save any changes to the database and close the connection.
    :param conn: connection to the database
    :param cursor: cursor to the database
    :return: None
    """
    conn.commit()
    cursor.close()
    conn.close()


def setup_db(cursor: Cursor, conn: Connection) -> None:
    """
    This function will create the jobs table if it doesn't already exist
    :param cursor: connection to the database
    :param conn: cursor to the database
    :return: None
    """
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS jobs(
        job_id TEXT PRIMARY KEY,
        job_title TEXT NOT NULL,
        company_name TEXT NOT NULL,
        job_description TEXT NOT NULL,
        location TEXT NOT NULL,
        min_salary INT DEFAULT 0,
        max_salary INT DEFAULT 0,
        salary_time TEXT DEFAULT 'yearly',
        posted_date TEXT,
        url TEXT NOT NULL,
        remote BOOLEAN DEFAULT FALSE);"""
    )
    conn.commit()


def insert_job(cursor: Cursor, conn: Connection, job_tuple: Tuple) -> None:
    """
    This function will insert a job into the jobs table.
    :param cursor: cursor to the database
    :param conn: connection to the database
    :param job_tuple: job tuple to be inserted into the database
    :return: None
    """
    sql_statement = """INSERT INTO jobs 
    (job_id, job_title, company_name, job_description, location, min_salary, max_salary, salary_time, posted_date, url, remote)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (job_id) DO NOTHING;"""
    cursor.execute(sql_statement, job_tuple)
    conn.commit()


def save_to_db(cursor: Cursor, all_jobs: list[Tuple]) -> None:
    """
    This function will save all jobs to the database.
    :param cursor: cursor to the database
    :param all_jobs: list of job tuples to be saved to the database
    :return: None
    """
    for job in all_jobs:
        try:
            insert_job(cursor, job)
        except Exception as e:
            print(f"Error inserting job into DB: {e}")

