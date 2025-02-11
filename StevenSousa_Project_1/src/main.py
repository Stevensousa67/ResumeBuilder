"""
Author: Steven Sousa
Prof.: John Santore
Institution: Bridgewater State University - COMP490 - Senior Design & Development
Version: 06Feb2025

Description: This program builds upon the achievements of Spring_1 main.py. In this version, the program can
programmatically parse the rapid_jobs2.json or rapidResults.json files in order to save each job into a PostgreSQL DB
and provide the ability to send any job from the DB as a prompt to Google AI Studio.
"""
# Import dependencies
import os
import dotenv
import DBUtils
import Data_Processing
import psycopg


def grab_job_description(conn: psycopg.Connection, cursor: psycopg.Cursor) -> str:
    """
    This function will grab a job description from the DB and return it as a string.

    :param conn: The database connection
    :param cursor: the database cursor
    :return: job description
    """


def main():

    # Load environment variables
    dotenv.load_dotenv(os.path.join(os.path.dirname(os.getcwd()), '.env'))

    # Connect using PostgresSQL default values
    conn_default, cursor_default = DBUtils.open_db(os.getenv('DB_NAME_DEFAULT'), os.getenv('DB_USER_DEFAULT'),
                                           os.getenv('DB_PASSWORD_DEFAULT'), os.getenv('DB_HOST'),
                                                   os.getenv('DB_PORT'), autocommit=True)

    # Create custom user
    DBUtils.create_user(cursor_default, os.getenv('DB_USER'), os.getenv('DB_PASSWORD'))

    # Create custom database
    DBUtils.create_db(cursor_default, os.getenv('DB_NAME'))

    # Assign newly created database to new user
    DBUtils.assign_ownership(cursor_default, os.getenv('DB_NAME'), os.getenv('DB_USER'))

    # Close existing connection in order to change databases
    DBUtils.close_db(conn_default, cursor_default)

    # Start new database connection using new
    conn, cursor = DBUtils.open_db(os.getenv('DB_NAME'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'),
                                   os.getenv('DB_HOST'), os.getenv('DB_PORT'), autocommit=False)
    # Create table in DB
    DBUtils.setup_table(conn, cursor)

    # Process data
    Data_Processing.process_json('../data/rapidResults.json', conn, cursor)

    # # Drop table
    # DBUtils.drop_table(conn, cursor)

    # # Generate resume
    # Generate_resume.generate_resume(os.getenv('GOOGLE_AI_API_KEY'), job_description, os.getenv('CONTACT_INFO'),
    #                                 os.getenv('SKILLS'), os.getenv('EDUCATION'), os.getenv('EXPERIENCE'),
    #                                 os.getenv('REFERENCES'), os.getenv('CONSTRAINTS'))

    # Exit program
    print('Program finished successfully.')


if __name__ == '__main__':
    main()
