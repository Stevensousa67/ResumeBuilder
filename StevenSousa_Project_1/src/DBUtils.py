"""
Author: Steven Sousa
Prof.: John Santore
Institution: Bridgewater State University - COMP490 - Senior Design & Development
Version: 06Feb2025

This program handles the creation of the PostgreSQL database utilized in Sprint 2. If a db already exists, it will do
 noting. Additionally, if a job_id already exists in the database, it won't add it again.
"""
from typing import Tuple

from psycopg import DatabaseError, Connection, Cursor, connect, sql


def open_db(dbname: str, user: str, password: str, host: str, port: str, autocommit: bool = False) -> (
        Tuple)[Connection, Cursor]:
    """
    This function will open a connection to the PostgreSQL database.
    :param dbname: os.getenv('DB_NAME')
    :param user: os.getenv('DB_USER')
    :param password: os.getenv('DB_PASSWORD')
    :param host: os.getenv('DB_HOST')
    :param port: os.getenv('DB_PORT')
    :param autocommit: True if you want to save changes automatically
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
        conn.autocommit = autocommit
        cursor = conn.cursor()
        return conn, cursor

    except (Exception, DatabaseError) as error:
        print(error)
        raise error


def create_user(cursor: Cursor, username: str, password: str):
    """
    This function will create a user in the PostgreSQL server
    :param cursor: cursor to the server
    :param username: username for the server
    :param password: password for the username
    :return:
    """
    # Create the user, if it doesn't exist
    cursor.execute(sql.SQL("SELECT 1 FROM pg_roles WHERE rolname = %s"), (username,))
    user_exists = cursor.fetchone()

    if not user_exists:
        cursor.execute(sql.SQL("CREATE USER {} WITH PASSWORD %S").format(sql.Identifier(username)), (password,))
        print(f'User {username} created successfully.')
    else:
        print(f'User {username} already exists.')


def create_db(cursor: Cursor, db_name):
    """
    This function will create a database in the PostgreSQL server
    :param cursor: cursor to the server
    :param db_name: name of the database
    :return:
    """

    cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), (db_name,))
    db_exists = cursor.fetchone()

    if not db_exists:
        cursor.execute(sql.SQL("CREATE DATABASE %s"), (db_name,))
        cursor.connection.commit()
        print(f'Database {db_name} created successfully.')
    else:
        print(f'Database {db_name} already exists.')


def assign_ownership(cursor: Cursor, db_name: str, username: str):
    """
    This function will assign ownership of a database to the specified user.
    :param cursor: cursor to the server
    :param db_name: database name
    :param username: owner username
    :return:
    """

    cursor.execute(sql.SQL("ALTER DATABASE {} OWNER TO {}").format(sql.Identifier(db_name),
                                                                   sql.Identifier(username)))


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


def setup_table(conn: Connection, cursor: Cursor) -> None:
    """
    This function will create the jobs table if it doesn't already exist
    :param cursor: connection to the database
    :param conn: cursor to the database
    :return: None
    """
    cursor.execute(sql.SQL(
        """CREATE TABLE IF NOT EXISTS jobs(
        job_id TEXT PRIMARY KEY,
        job_title TEXT NOT NULL,
        company_name TEXT NOT NULL,
        job_description TEXT NOT NULL,
        location TEXT NOT NULL,
        min_salary DECIMAL DEFAULT 0,
        max_salary DECIMAL DEFAULT 0,
        salary_time TEXT DEFAULT 'yearly',
        posted_date TEXT,
        url TEXT NOT NULL,
        remote BOOLEAN DEFAULT FALSE);"""
    ))
    conn.commit()


def insert_job(conn: Connection, cursor: Cursor, job_tuple: Tuple) -> None:
    """
    Inserts a job into the jobs table.
    :param cursor: cursor to the database
    :param conn: connection to the database
    :param job_tuple: job_tuple: Tuple containing job details
    :return: None
    """
    cursor.execute(sql.SQL(
        """INSERT INTO jobs
        (job_id, job_title, company_name, job_description, location, min_salary, max_salary, salary_time, posted_date,
         url, remote)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (job_id) DO NOTHING;
    """), job_tuple)
    conn.commit()


def drop_table(conn: Connection, cursor: Cursor) -> None:
    """ This function will drop the job table in the DB.
    :param cursor: cursor to the database
    :param conn: connection to the database
    :return: None
    """
    cursor.execute(sql.SQL("""DROP TABLE IF EXISTS jobs RESTRICT;"""))
    conn.commit()
    cursor.close()
    conn.close()


def retrieve_job(cursor: Cursor) -> Tuple:
    """
    This function will retrieve a job from the DB.
    :param cursor: cursor to the database
    :return: job
    """
    cursor.execute(sql.SQL("""SELECT * FROM jobs WHERE job_id = %s"""))
    return cursor.fetchone()
