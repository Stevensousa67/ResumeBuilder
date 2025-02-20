"""
Author: Steven Sousa
Prof.: John Santore
Institution: Bridgewater State University - COMP490 - Senior Design & Development
Version: 06Feb2025

Description: In this version, the program will programmatically parse the rapid_jobs2.json or rapidResults.json files
in order to save each job into a PostgreSQL DB.
"""
# Import dependencies
import os
import dotenv
from src import DBUtils
from src import Data_Processing


def main():

    # Load environment variables
    dotenv.load_dotenv()

    # # Connect using GCP PostgresSQL default values
    # conn_default, cursor_default = DBUtils.open_db(
    #     os.getenv('GCP_DB_NAME_DEFAULT'),
    #     os.getenv('GCP_DB_USER_DEFAULT'),
    #     os.getenv('GCP_DB_PASSWORD_DEFAULT'),
    #     os.getenv('GCP_DB_HOST'),
    #     os.getenv('GCP_DB_PORT'),
    #     autocommit=True
    # )

    # Connect using localhost PostgresSQL default values
    conn_default, cursor_default = DBUtils.open_db(
        os.getenv('DB_NAME_DEFAULT'),
        os.getenv('DB_USER_DEFAULT'),
        os.getenv('DB_PASSWORD_DEFAULT'),
        os.getenv('DB_HOST_DEFAULT'),
        os.getenv('DB_PORT_DEFAULT'),
        autocommit=True
    )

    # Create custom user
    DBUtils.create_user(cursor_default, os.getenv('DB_USER'), os.getenv('DB_PASSWORD'))

    # Create custom database
    DBUtils.create_db(cursor_default, os.getenv('DB_NAME'))

    # Close existing connection in order to change databases
    DBUtils.close_db(conn_default, cursor_default)

    # # Start new GCP database connection newly created database
    # conn, cursor = DBUtils.open_db(
    #     os.getenv('DB_NAME'),
    #     os.getenv('DB_USER'),
    #     os.getenv('DB_PASSWORD'),
    #     os.getenv('GCP_DB_HOST'),
    #     os.getenv('GCP_DB_PORT'),
    #     autocommit=False
    # )

    # Start new local database connection using newly created database
    conn, cursor = DBUtils.open_db(
        os.getenv('DB_NAME'),
        os.getenv('DB_USER'),
        os.getenv('DB_PASSWORD'),
        os.getenv('DB_HOST_DEFAULT'),
        os.getenv('DB_PORT_DEFAULT'),
        autocommit=False
    )

    # Create table in DB
    DBUtils.setup_table(conn, cursor)

    # Process data
    print("\nInserting data from rapidResults.json to cloud database, please wait...")
    Data_Processing.process_json('data/rapidResults.json', conn, cursor)
    print("Data from rapidResults.json inserted successfully.")
    print("\nInserting data from rapid_jobs2 to cloud database, please wait...")
    Data_Processing.process_json('data/rapid_jobs2.json', conn, cursor)
    print("Data from rapid_jobs2.json inserted successfully.")

    # # Drop table
    # DBUtils.drop_table(conn, cursor)
    # print("Table dropped successfully.")

    # Exit program
    print('Program finished successfully.')


if __name__ == '__main__':
    main()
